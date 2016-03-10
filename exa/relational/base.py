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
__all__ = ['_create_all']


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
    def __len__(self):
        session = SessionMaker()
        n = session.query(self).count()
        session.close()
        return n

    def __iter__(self):
        session = SessionMaker()
        for item in session.query(self).all():
            yield item
        session.close()

    def __getitem__(self, key):
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
            obj = session.query(self).filter(self.pkid == key).one()
        elif isinstance(key, str) and hasattr(self, 'name'):
            obj = session.query(self).filter(self.name == key).one()
        elif isinstance(key, UUID) and hasattr(self, 'uid'):
            obj = session.query(self).filter(self.uid == key.hex).one()
        elif hasattr(self, '_getitem'):
            obj = self._getitem(key, session)
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

            [{'column1': 'foo', 'column2': 42, 'column3': 'bar'}]

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
    '''
    name = Column(String)
    description = Column(String)


class HexUID:
    '''
    Mixin when a unique ID is required.
    '''
    hexuid = Column(String(32), default=uid)

    @property
    def uid(self):
        return UUID(self.hexuid)


class Time:
    '''
    Mixin for when date and time stamps for created, accessed, and modified
    are required
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


@event.listens_for(mapper, 'init')             # Any time an object is created,
def add_to_db(obj, args, kwargs):              # add it to the database session
    '''
    All relational objects are automatically added to the database session on
    instantiation.
    '''
    db_sess.add(obj)


@event.listens_for(Query, 'before_compile')    # Always commit before querying (SELECT)
def commit(*args, **kwargs):
    '''
    Commit all of the objects currently in the session. Note that objects
    are automatically added to the database session (db_sess) and that committing
    these objects does not normally have to be performed manually.
    '''
    pass
    #try:
    #    db_sess.commit()
    #except:
    #    db_sess.rollback()
    #    raise


@event.listens_for(Base, 'before_insert')            # Before inserting a new object
def base_before_insert(mapper, connection, target):  # update its timestamps.
    '''
    Update timestampes and save :class:`~exa.frames.DataFrame` data to disk
    before inserting to the database.
    '''
    print('before insert')


@event.listens_for(Base, 'before_update')            # Before inserting a new object
def base_before_update(mapper, connection, target):  # update its timestamps.
    '''
    Update timestampes and save :class:`~exa.frames.DataFrame` data to disk
    before updating the database.
    '''
    print('before update')


engine_name = _conf['exa_relational']
engine = create_engine(engine_name)
SessionMaker = sessionmaker(bind=engine)
