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
    def to_frame(cls):
        """
        Convenience method for converting table to :class:`~pandas.DataFrame`.

        Warning:
            This method should not generally be used see :mod:`~exa.cms.mgmt`
            for ways of extracting/inspecting database data.
        """
        with scoped_session() as session:
            statement = session.query(cls).statement
            df = pd.read_sql(statement, engine)
            if 'pkid' in df:
                df.set_index('pkid', inplace=True)
                df = df.sort_index()
            return df

    def delete(cls, pkid):
        # Can only delete by pkid
        with scoped_session() as session:
            session.query(cls).filter(cls.pkid == pkid).delete()

    def get_by_pkid(cls, pkid):
        """Select an object by pkid."""
        obj = session_factory().query(cls).get(pkid)
        if obj is None:
            raise KeyError("Entry with pkid {} not found in {}".format(str(pkid), cls.__name__))
        return obj

    def get_by_name(cls, name):
        """Select objects by name."""
        return session_factory().query(cls).filter(cls.name == name).all()

    def get_by_uid(cls, uid):
        """Select an object by hexuid (as string)"""
        return session_factory().query(cls).filter(cls.uid == uid).one()

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
            return cls.get_by_uid(key)
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

    def to_series(self):
        """
        Create a series object from the given record entry.
        """
        s = pd.Series(self.__dict__)
        del s['_sa_instance_state']
        return s

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

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
    modified = Column(DateTime)

    def update_modified(self):
        """Update the modified timestamp to now."""
        self.modified = datetime.now()


class Size(object):
    """Approximate size (on disk) and file count fields."""
    size = Column(Integer)
    nfiles = Column(Integer)


session_factory = None
reconfigure_session_factory()
