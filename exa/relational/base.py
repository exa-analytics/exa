# -*- coding: utf-8 -*-
'''
Relational
===============================================
This modules provides the base class for persitent relational objects such as the
:class:`~exa.relational.container.Container` object. It defines a declarative base class that has
convenience methods for looking up database entries by common features and returning and appropriate
and corresponding dataframe or series object.
'''
import pandas as pd
from sys import getsizeof
from uuid import UUID, uuid4
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa import exa_global_config


gen_uid = lambda: uuid4().hex
config = {'engine_name': None, 'engine': None, 'SessionFactory': None}


class BaseMeta(DeclarativeMeta):
    '''
    The base relational class object definition. The class object has convenience methods for
    quick lookup and conversion of relational data to usable objects such as dataframes and series.
    '''
    def get_by_pkid(self, pkid):
        '''
        Select a single entry using the primary key.
        '''
        with scoped_session() as s:
            obj = s.query(self).filter(self.pkid == pkid).one()
        return obj

    def get_by_str(self, string):
        '''
        Select objects by name.
        '''
        with scoped_session() as s:
            objs = s.query(self).filter(self.name == string).all()
        return objs

    def get_by_uid(self, uid):
        '''
        Select an entry by unique ID.
        '''
        hexuid = uid
        if isinstance(uid, uuid.UUID):
            hexuid = uid.hex
        with scoped_session() as s:
            obj = s.query(self).filter(self.hexuid == hexuid).one()
        return obj

    def _bulk_insert(self, data):
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
        with scoped_session() as session:
            session.bulk_insert_mappings(self, data)

    def table(self):
        '''
        Create a DataFrame representation of the current table.

        Returns:
            df (:py:class:`~pandas.DataFrame`): In memory table copy

        Warning:
            If performing this action on a very large table, may raise a
            memory error. In this case it is more effective to perform a
            custom select query then convert the result to a DataFrame.
        '''
        with scoped_session() as s:
            df = pd.read_sql(s.query(self).statement, config['engine'])
        if 'pkid' in df:
            df = df.set_index('pkid').sort_index()
        return df

    def __contains__(self, obj):
        tbl = self.table()
        for col in tbl:
            if obj in tbl[col]:
                return True
            elif hasattr(self, 'aliases'):
                if obj in self.aliases:
                    if self.aliases[obj] in tbl[col]:
                        return True
        return False

    def __iter__(self):
        with scoped_session() as s:
            for item in s.query(self).all():
                yield item

    def __getitem__(self, key):
        if hasattr(self, 'getitem'):
            obj = self.getitem(key)
        elif isinstance(key, int):
            obj = self.get_by_pkid(key)
        elif isinstance(key, str):
            obj = self.get_by_str(key)
        elif isinstance(key, UUID):
            obj = self.get_by_uid(key)
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

    def _save(self):
        '''
        Save the relational object to the database.
        '''
        self._s = config['SessionFactory'](expire_on_commit=False)
        self._s.add(self)
        self._s.commit()

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



def create_tables():
    '''
    Create all tables if they do not already exist in the database.

    Note:
        When this function is called, only class objects loaded in the current
        namespace will be created.
    '''
    Base.metadata.create_all(config['engine'])


def init_db():
    '''
    Initialize the database connection and session factory.
    '''
    global config
    config['engine_name'] = exa_global_config['exa_relational']
    config['engine'] = create_engine(config['engine_name'])
    config['SessionFactory'] = sessionmaker(bind=config['engine'])


def cleanup():
    '''
    Cleanup the engine's connection pool before exiting.
    '''
    config['engine'].dispose()


@contextmanager
def scoped_session(*args, **kwargs):
    '''
    Separation of transaction management from actual work using a `context manager`_.

    .. _context manager: http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
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

init_db()
