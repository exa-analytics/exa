# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Base Table Model
##################################################
This module provides the base classes and metaclasses for database tables.
"""
import hashlib
import pandas as pd
from sys import getsizeof
from numbers import Integral
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa._config import engine


@contextmanager
def scoped_session(*args, **kwargs):
    """Safely commit relational objects."""
    session = session_factory(*args, **kwargs)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def reconfigure_session_factory():
    """Internal function for binding the session_factory attribute to the engine."""
    global session_factory
    session_factory = sessionmaker(bind=engine)


class BaseMeta(DeclarativeMeta):
    """
    This is the base metaclass for all relational tables. It provides convient
    lookup methods, bulk insert methods, and conversions to other formats.
    """
    def get_by_pkid(cls, pkid):
        """Select an object by pkid."""
        return session_factory().query(cls).get(pkid)

    def get_by_name(cls, name):
        """Select objects by name."""
        return session_factory().query(cls).filter(cls.name == name).all()

    def get_by_uid(cls, uid):
        """Select an object by hexuid (as string)"""
        return session_factory().query(cls).filter(cls.uid == uid).one()

    def bulk_insert(cls, mappings):
        """
        Perform a `bulk insert`_ into a specific table.

        .. code-block:: Python

            mappings = [{'column1': 'foo', 'column2': 42, 'column3': 'bar'},
                        {'column1': 'fop', 'column2': 43, 'column3': 'baz'}]
            Table.bulk_insert(mappings)

        .. _bulk insert: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        """
        with scoped_session() as session:
            session.bulk_insert_mappings(cls, mappings)


    def __getitem__(cls, key):
        """
        Custom getter allows for the following convenient syntax:

        .. code-block:: Python

            exa.relational.File[1]            # Gets file with pkid == 1
            exa.relational.File['name']       # Gets file with name == 'name'
            exa.relational.Isotope['H']       # Gets isotopes with symbol == 'H'
            exa.relational.Isotope['12C']     # Gets isotope with strid == '12C'
            exa.relational.Length['m', 'km']  # Gets conversion factor meters to kilometers
        """
        if hasattr(cls, '_getitem'):         # First try using custom getter
            return cls._getitem(key)
        elif isinstance(key, Integral):
            return cls.get_by_pkid(key)
        elif isinstance(key, str) and len(key) == 64:
            return cls.get_by_sha256(key)
        elif isinstance(key, str):
            return cls.get_by_name(key)
        raise KeyError('Unknown key ({0}).'.format(key))


@as_declarative(metaclass=BaseMeta)
class Base(object):
    """
    Base class for all relational tables. These classes behave as both the
    definition of the table (the schema) as well as an object instance (in a
    Python environment) of an entry (row) in the table.
    """
    pkid = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_series(self):
        """
        Create a series object from the given record entry.
        """
        s = pd.Series(self.__dict__)
        del s['_sa_instance_state']
        return s

    def _save_record(self):
        """
        Save the current object's relational information.
        """
        session = session_factory(expire_on_commit=False)
        session.add(self)
        session.commit()

    def __repr__(self):
        return '{0}(pkid: {1})'.format(self.__class__.__name__, self.pkid)


class Name(object):
    """Name and description fields."""
    name = Column(String)
    description = Column(String)


class Sha256UID(object):
    """SHA-256 unique ID field."""
    uid = Column(String(64), nullable=False)

    @staticmethod
    def sha256_from_file(path, blocksize=65536):
        """Compute sha-256 hash of a file."""
        sha = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(blocksize), b""):
                sha.update(chunk)
        return sha.hexdigest()


class Time(object):
    """Timestamp fields."""
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def _update_accessed(self):
        self.accessed = datetime.now()

    def _update_modified(self):
        self.modified = datetime.now()


class Size(object):
    """Approximate size (on disk) and file count fields."""
    size = Column(Integer)
    nfiles = Column(Integer)

    def _update(self):
        self.size = getsizeof(self)


session_factory = None
reconfigure_session_factory()
