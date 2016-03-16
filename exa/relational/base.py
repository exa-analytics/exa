# -*- coding: utf-8 -*-
'''
Base Table for Relational Objects
===============================================
This module outlines the event-based content management system established by exa and creates
a complex base table (schema) class, :class:`~exa.relational.base.Base`. The schema base class's
metaclass inherits the metaclass of :py:class:`~ipywidgets.DOMWidget` in order for certain
tables to be able to have HTML representations (within the `Jupyter notebook`_).

.. _Jupyter notebook: http://jupyter.org/
'''
import pandas as pd
from uuid import UUID
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa import _conf
from exa.utility import uid as _uid


class BaseMeta(DeclarativeMeta):
    '''
    This class defines the behavior of the :class:`~exa.relational.base.Base`
    object. It provides methods for convenient class level look up.
    '''
    def _get_by_pkid(self, pkid):
        '''
        Select a single entry using the primary key.

        Returns:
            entry: Single entry with given pkid
        '''
        return SessionFactory().query(self).filter(self.pkid == pkid).one()

    def _get_by_str(self, string):
        '''
        Select entries using a string identifier: first tries to find objects
        using the "name" field then by alternate fields.

        Returns:
            data (list): List of matching entries
        '''
        value = None
        session = SessionFactory()
        if hasattr(self, 'name'):
            value = session.query(self).filter(self.name == string).all()
        elif hasattr(self, 'symbol'):
            value = session.query(self).filter(self.symbol == string).all()
            if len(value) == 1:
                value = value[0]
        elif hasattr(self, 'from_unit'):
            value = session.query(self).filter(self.from_unit == string).all()
        else:
            session.close_all()
            raise TypeError('Selection by string arguments not supported for {}'.format(self.__name__))
        return value

    def _get_by_uid(self, uid):
        '''
        Select an entry using a unique ID.

        Returns:
            entry: Single entry with given uid
        '''
        if isinstance(uid, uuid.UUID):
            return SessionFactory().query(self).filter(self.hexuid == uid.hex).one()
        elif isinstance(uid, str):
            return SessionFactory().query(self).filter(self.hexuid == uid).one()
        else:
            raise TypeError('uid must be of type str or UUID, not {}'.format(type(uid)))

    def __contains__(self, obj):
        '''
        Can check if conversions for a specific unit exist.

        .. code-block:: Python

            'A' in exa.relational.Length
        '''
        if hasattr(self, 'from_unit'):
            from_unit = self.table()['from_unit'].values
            if obj in self.aliases:
                obj = self.aliases[obj]
            if obj in from_unit:
                return True
        else:
            raise NotImplementedError()
        return False

    def __iter__(self):
        for item in SessionFactory().query(self).all():
            yield item

    def __getitem__(self, key):
        obj = None
        if isinstance(key, int):
            obj = self._get_by_pkid(key)
        elif isinstance(key, str):
            obj = self._get_by_str(key)
        elif isinstance(key, UUID):
            obj = self._get_by_uid(key)
        if obj is None and hasattr(self, '_getitem'):
            obj = self._getitem(key)
        return obj


@as_declarative(metaclass=BaseMeta)
class Base:
    '''
    Declarative base class (used by SQLAlchemy) to initialize relational tables.
    '''
    pkid = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def _bulk_insert(cls, data):
        '''
        Perform a `bulk insert`_ into a specific table.

        .. code-block:: Python

            mappings = [{'column1': 'foo', 'column2': 42, 'column3': 'bar'},
                        {'column1': 'fop', 'column2': 43, 'column3': 'baz'}]
            Table.bulk_insert(mappings)

        Args:
            data (list): List of records as dictionary objects

        .. _bulk insert: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        '''
        with session_scope() as session:
            session.bulk_insert_mappings(cls, data)

    @classmethod
    def table(cls):
        '''
        Create a DataFrame representation of the current table.

        Returns:
            df (:py:class:`~pandas.DataFrame`): In memory table copy

        Warning:
            If performing this action on a very large table, may raise a
            memory error. In this case it is more effective to perform a
            custom select query then convert the result to a DataFrame.
        '''
        df = None
        with session_scope() as session:
            df = pd.read_sql(session.query(cls).statement, engine)
        if 'pkid' in df.columns:
            df.set_index('pkid', inplace=True)
        for column in df.columns:    # Mask the auxiliary pkid columns if applicable
            if 'id' in column and len(column) == 4:
                if df.index.names == ['pkid']:
                    del df[column]
                else:
                    df.set_index(column, inplace=True)
                    df.index.names = ['pkid']
        return df

    def _save_record(self):
        '''
        Save the relational object to the database.
        '''
        session = SessionFactory(expire_on_commit=False)
        session.add(self)
        session.commit()
        
    def __repr__(cls):
        return '{0}(pkid: {1})'.format(cls.__class__.__name__, cls.pkid)


class Name:
    '''
    Mixin providing name and description fields.
    '''
    name = Column(String)
    description = Column(String)


class HexUID:
    '''
    Mixin providing a unique ID.
    '''
    hexuid = Column(String(32), default=_uid)

    @property
    def uid(self):
        return UUID(self.hexuid)


class Time:
    '''
    Mixin providing timestamp information.
    '''
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def _update_accessed(self):
        self.accessed = datetime.now()

    def _update_modified(self):
        self.modified = datetime.now()


class Disk:
    '''
    Mixin providing disk utilization information.

    Attributes:
        nfiles (int): Number of associated files (in the file table)
        size (int): Total size on disk (in KiB) (of all files)

    See Also:
        :class:`~exa.relational.file.File`
    '''
    nfiles = Column(Integer)
    size = Column(Integer)


def _create_all():
    '''
    Create all tables if they do not already exist in the database.

    Warning:
        When this function is called only class objects loaded in the current
        namespace will be created.
    '''
    Base.metadata.create_all(engine)


def _cleanup():
    '''
    Cleanup the engine's connection pool before exiting.
    '''
    engine.dispose()


@contextmanager
def session_scope(*args, **kwargs):
    '''
    Separation of transaction management from actual work using a `context manager`_.

    .. _context manager: http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    '''
    session = SessionFactory(*args, **kwargs)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()    # Occurs regardless if an exception is raised or not


engine_name = _conf['exa_relational']
engine = create_engine(engine_name)
SessionFactory = sessionmaker(bind=engine)
