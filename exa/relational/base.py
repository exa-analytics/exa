# -*- coding: utf-8 -*-
'''
Base Classes for Content Management
#########################################
'''
import pandas as pd
from numbers import Integral
from sys import getsizeof
from uuid import UUID, uuid4
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa._config import config
from exa.log import get_logger


gen_uid = lambda: uuid4().hex


class BaseMeta(DeclarativeMeta):
    '''
    This is the base metaclass for all relational tables. It provides convient
    lookup methods, bulk insert methods, and a conversion to dataframe.
    '''
    def get_by_pkid(cls, pkid):
        '''
        Select a single entry using the primary key.
        '''
        with scoped_session() as s:
            return s.query(cls).get(pkid)

    def get_by_name(cls, name):
        '''
        Select objects with the given name.
        '''
        with scoped_session() as s:
            return s.query(cls).filter(cls.name == name).all()

    def get_by_uid(cls, uid):
        '''
        Select an entry by unique ID.
        '''
        hexuid = uid
        if isinstance(uid, uuid.UUID):
            hexuid = uid.hex
        with scoped_session() as s:
            return s.query(cls).filter(cls.hexuid == hexuid).one()

    def bulk_insert(cls, mappings):
        '''
        Perform a `bulk insert`_ into a specific table.

        .. code-block:: Python

            mappings = [{'column1': 'foo', 'column2': 42, 'column3': 'bar'},
                        {'column1': 'fop', 'column2': 43, 'column3': 'baz'}]
            Table.bulk_insert(mappings)

        .. _bulk insert: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        '''
        with scoped_session() as s:
            s.bulk_insert_mappings(cls, mappings)

    def to_frame(self):
        '''
        Create a DataFrame representation of the current table.

        Warning:
            If performing this action on a very large table, may raise a
            memory error. It is almost always more effective to query the
            table for the specific records of interest.
        '''
        with scoped_session() as s:
            df = pd.read_sql(s.query(self).statement, config['engine'])
            if 'pkid' in df:
                df = df.set_index('pkid').sort_index()
            return df

    def __getitem__(cls, key):
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
    The base class for all relational tables. Relational classes define both the database table
    schema as well as an entry instance object. Relational classes have convience lookup methods
    for fast, Python database querying, which abstracts away SQL interactions.
    '''
    pkid = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_series(self):
        '''
        Create a :class:`~exa.numerical.Series` object from the current record.
        '''
        s = pd.Series(self.__dict__)
        del s['_sa_instance_state']
        return s

    def _save_record(self):
        '''
        Save the current object.
        '''
        with scoped_session(expire_on_commit=False) as s:
            s.add(self)

    def __repr__(self):
        return '{0}(pkid: {1})'.format(self.__class__.__name__, self.pkid)


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
    hexuid = Column(String(32), default=gen_uid)

    @property
    def uid(self):
        return UUID(self.hexuid)

    def gen_uid(self):
        return gen_uid()


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

    def _update_size(self):
        '''
        Attempts to call the instance's __sizeof__ to populate the value of
        size.
        '''
        try:
            self.size = getsizeof(self)
        except:
            pass


def create_db():
    '''
    Modifies the package-wide configuration object (:mod:`~exa._config`),
    adding the database engine and SessionFactory objects.
    '''
    global config
    config['engine'] = create_engine(config['exa_relational'])
    config['SessionFactory'] = sessionmaker(bind=config['engine'])
    Base.metadata.create_all(config['engine'])


def cleanup_db():
    '''
    Dispose the database engine.
    '''
    config['engine'].dispose()
    del config['engine']
    del config['SessionFactory']


@contextmanager
def scoped_session(*args, **kwargs):
    '''
    A thread scoped session object.
    '''
    session = config['SessionFactory'](*args, **kwargs)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
