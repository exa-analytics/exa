# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Database Engine Configuration
##################################################
This module provides the base classes and metaclasses for relational tables
created by exa. It also provides the database engine configuration and session
class factory.
'''
import atexit
import pandas as pd
from sys import getsizeof
from uuid import UUID, uuid4
from numbers import Integral
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa._config import config
from exa.log import loggers


def generate_hexuid():
    '''Create a unique, random, hex string id.'''
    return uuid4().hex


def cleanup_engine():
    '''At exit, cleanup connection pool.'''
    engine.dispose()


@contextmanager
def scoped_session(*args, **kwargs):
    '''Safely commit relational objects.'''
    session = session_factory(*args, **kwargs)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class BaseMeta(DeclarativeMeta):
    '''
    This is the base metaclass for all relational tables. It provides convient
    lookup methods, bulk insert methods, and conversions to other formats.
    '''
    def get_by_pkid(cls, pkid):
        '''Select an object by pkid.'''
        return session_factory().query(cls).get(pkid)

    def get_by_name(cls, name):
        '''Select objects by name.'''
        return session_factory().query(cls).filter(cls.name == name).all()

    def get_by_uid(cls, uid):
        '''Select an object by hexuid (as string)'''
        hexuid = uid
        if isinstance(uid, UUID):
            hexuid = uid.hex
        return session_factory().query(cls).filter(cls.hexuid == hexuid).one()

    def bulk_insert(cls, mappings):
        '''
        Perform a `bulk insert`_ into a specific table.

        .. code-block:: Python

            mappings = [{'column1': 'foo', 'column2': 42, 'column3': 'bar'},
                        {'column1': 'fop', 'column2': 43, 'column3': 'baz'}]
            Table.bulk_insert(mappings)

        .. _bulk insert: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        '''
        with scoped_session() as session:
            session.bulk_insert_mappings(cls, mappings)

    def to_frame(cls):
        '''
        Dump the table to a :class:`~pandas.DataFrame` object.

        Warning:
            If performing this action on a very large table, may raise a
            memory error. It is almost always more effective to query the
            table for the specific records of interest.
        '''
        statement = session_factory().query(cls).statement
        df = pd.read_sql(statement, engine)
        if 'pkid' in df:
            df = df.set_index('pkid').sort_index()
        return df

    def __getitem__(cls, key):
        '''
        Custom getter allows for the following convenient syntax:

        .. code-block:: Python

            exa.relational.File[1]            # Gets file with pkid == 1
            exa.relational.File['name']       # Gets file with name == 'name'
            exa.relational.Isotope['H']       # Gets isotopes with symbol == 'H'
            exa.relational.Isotope['12C']     # Gets isotope with strid == '12C'
            exa.relational.Length['m', 'km']  # Gets conversion factor meters to kilometers
        '''
        obj = None
        if hasattr(cls, '_getitem'):         # First try using custom getter
            obj = cls._getitem(key)
        if obj is None:                      # Fall back to default getters
            if isinstance(key, Integral):
                return cls.get_by_pkid(key)
            elif isinstance(key, UUID):
                return cls.get_by_uid(key)
            elif isinstance(key, str):
                return cls.get_by_name(key)
            else:
                raise KeyError('Unknown key ({0}).'.format(key))
        return obj


@as_declarative(metaclass=BaseMeta)
class Base:
    '''
    Base class for all relational tables. These classes behave as both the
    definition of the table (the schema) as well as an object instance (in a
    Python environment) of an entry (row) in the table.
    '''
    pkid = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_series(self):
        '''
        Create a series object from the given record entry.
        '''
        s = pd.Series(self.__dict__)
        del s['_sa_instance_state']
        return s

    def _save_record(self):
        '''
        Save the current object's relational information.
        '''
        session = session_factory(expire_on_commit=False)
        session.add(self)
        session.commit()

    def __repr__(self):
        return '{0}(pkid: {1})'.format(self.__class__.__name__, self.pkid)


# These are so-called "mix-in" classes that add specific fields to a table
class Name:
    '''Name and description fields.'''
    name = Column(String)
    description = Column(String)


class HexUID:
    '''Hex-based unique id (uid) field.'''
    hexuid = Column(String(32), default=generate_hexuid)

    @property
    def uid(self):
        return UUID(self.hexuid)


class Time:
    '''Timestamp fields.'''
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def _update_accessed(self):
        self.accessed = datetime.now()

    def _update_modified(self):
        self.modified = datetime.now()


class Size:
    '''Approximate size (on disk) and file count fields.'''
    size = Column(Integer)
    nfiles = Column(Integer)

    def _update(self):
        self.size = getsizeof(self)


logger = loggers['dblog']
engine = create_engine(config['db']['uri'])
session_factory = sessionmaker(bind=engine)
