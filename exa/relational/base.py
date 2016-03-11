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
from sqlalchemy import Column, Integer, String, DateTime, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa import _conf
from exa.utility import uid


class BaseMeta(DeclarativeMeta):
    '''
    This class defines the :class:`~exa.relational.base.Base` class instance.
    Its primary function is to allow custom variable getting at the class
    object level:

    .. code:: Python

        obj = exa.relational.base.Meta['some key']
    '''
    def __len__(cls):
        session = SessionMaker()
        n = session.query(cls).count()
        session.close()
        return n

    def __contains__(cls, obj):
        '''
        Can check if conversions for a specific unit exist.

        .. code-block:: Python

            'A' in exa.relational.Length
        '''
        if hasattr(cls, 'from_unit'):
            from_unit = cls.table()['from_unit'].values
            if obj in cls.aliases:
                obj = cls.aliases[obj]
            if obj in from_unit:
                return True
        else:
            raise NotImplementedError()
        return False


    def __iter__(cls):
        session = SessionMaker()
        for item in session.query(cls).all():
            yield item
        session.close()

    def __getitem__(cls, key):
        '''
        This is called when a user attempts to slice/select an entry from the
        database table (the metaclass of the object is a representation of the
        table). This is not the getitem function that is called when a user
        attempts to slice an entry instance.

        .. code-block:: Python

            c = exa.Container[1]    # Loads the container with pkid == 1 (via this __getitem__)
            c[1]      # Slices the first (multiindex) level of each dataframe attached to this
            c[::4]    # container (via the :class:`~exa.relational.container.Container`'s __getitem__)

        '''
        session = SessionMaker()
        obj = None
        if isinstance(key, int):
            obj = session.query(cls).filter(cls.pkid == key).one()
        elif isinstance(key, str) and hasattr(cls, 'name'):
            obj = session.query(cls).filter(cls.name == key).one()
        elif isinstance(key, UUID) and hasattr(cls, 'uid'):
            obj = session.query(cls).filter(cls.uid == key.hex).one()
        elif hasattr(cls, '_getitem'):
            obj = cls._getitem(key, session)
        else:
            raise KeyError('Unknown key {0}.'.format(key))
        session.close()
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
    def bulk_insert(cls, data):
        '''
        Perform a bulk insert into a specific table.

        .. code-block:: Python

            mappings = [{'column1': 'foo', 'column2': 42, 'column3': 'bar'}]
            Table.bulk_insert(mappings)

        Args:
            data (list): List of dictionary objects (mappings - see the example above)
        '''
        session = SessionMaker()
        try:
            session.bulk_insert_mappings(cls, data)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def table(cls, force_full=False):
        '''
        Args:
            force_full (bool): Force return of the complete table

        Returns:
            df (:py:class:`~pandas.DataFrame`): In memory table copy
        '''
        session = SessionMaker()
        df = pd.read_sql(session.query(cls).statement, engine)
        session.close()
        if 'pkid' in df.columns:
            df.set_index('pkid', inplace=True)
        return df

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
    hexuid = Column(String(32), default=uid)

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

    def update_accessed(self):
        self.accessed = datetime.now()

    def update_modified(self):
        self.modified = datetime.now()


class Disk:
    '''
    Mixin providing disk utilization information.
    '''
    size = Column(Integer)
    file_count = Column(Integer)


def _create_all():
    '''
    Create all tables if they do not already exist in the database.

    Note:
        When this function is called only class objects loaded in the current
        namespace will attempt to be created.
    '''
    Base.metadata.create_all(engine)


engine_name = _conf['exa_relational']
engine = create_engine(engine_name)
SessionMaker = sessionmaker(bind=engine)
