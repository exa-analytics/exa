# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa
#########
"""
import os
import sys
import datetime as dt
import logging.config
import yaml
from pathlib import Path
from traitlets import HasTraits, Unicode, Instance, default, validate


_base = os.path.abspath(os.path.dirname(__file__))


class Base(HasTraits):
    """A traitlets base class that provides configuration
    and logging utilities. Subclasses define respective
    traits and trait-based logic.
    """

    @default('name')
    def _default_name(self):
        return self.__class__.__name__

    @validate('name')
    def _validate_name(self, prop):
        name = prop.value
        self.log.debug(f"lowercasing {name}")
        return name.lower()

    @staticmethod
    def right_now():
        """Returns the current datetime"""
        return dt.datetime.now()

    @staticmethod
    def time_diff(start):
        """Returns a formatted string of the time difference
        between right now and the passed in datetime"""
        stop = dt.datetime.now()
        return '{:.2f}s'.format((stop - start).total_seconds())

    @property
    def log(self):
        """A configured `logger` object"""
        name = '.'.join([
            self.__module__, self.__class__.__name__
        ])
        return logging.getLogger(name)

    def to_yml(self, path):
        with open(path, 'w') as f:
            yaml.dump(self.traits(), f, default_flow_style=False)

    @classmethod
    def from_yml(cls, path):
        """Load an object from a configuration file"""
        return cls(**cls._from_yml(path))

    @staticmethod
    def _from_yml(path):
        """Load a configuration file"""
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f.read())
        return cfg

    def traits(self, *args, **kws):
        """Return the set of traits specified in exa"""
        skipme = ['parent', 'config']
        traits = super().traits(*args, **kws)
        return {k: v for k, v in traits.items()
                if k not in skipme}

    def trait_items(self, include_falsy=False):
        """Return a dictionary of trait names and values"""
        if include_falsy:
            return {k: getattr(self, k) for k in self.traits()}
        return {k: getattr(self, k) for k in self.traits()
                if getattr(self, k)}


class Cfg(Base):
    """Exa library configuration object. Manages logging
    configuration and the static asset resource API and
    external application integrations.
    """
    logdir = Unicode()
    savedir = Instance(Path)
    logname = Unicode()
    staticdir = Unicode()

    @property
    def db_conn(self):
        """Environment configured database connection string.
        Should be a valid sqlalchemy engine connection string.

        Note:
            Make sure your database is running

        Examples of valid EXA_DB_CONN values:
            EXA_DB_CONN='sqlite://'
            EXA_DB_CONN='postgresql://username:password@localhost:5432/dbname'
        """
        return os.getenv('EXA_DB_CONN', '')

    @validate('logdir')
    def _validate_logdir(self, prop):
        logdir = prop['value']
        self.log.debug(f"making sure {logdir} exists")
        os.makedirs(logdir, exist_ok=True)
        return prop['value']

    @default('logdir')
    def _default_logdir(self):
        base = os.path.expanduser('~')
        base = os.path.join(base, '.exa')
        self.log.debug(f"initializing with logdir {base}")
        return base

    @default('savedir')
    def _default_savedir(self):
        return Path(self._default_logdir())

    @default('staticdir')
    def _default_staticdir(self):
        base = os.path.join(_base, "static")
        self.log.debug(f"initializing with staticdir {base}")
        return base

    def resource(self, name):
        """Return the full path of a named resource
        in the static directory.

        If multiple files with the same name exist,
        **name** should contain the first directory
        as well.

        .. code-block:: python

            import exa
            exa.cfg.resource("myfile")
            exa.cfg.resource("test01/test.txt")
            exa.cfg.resource("test02/test.txt")
        """
        for path, _, files in os.walk(self.staticdir):
            if name in files:
                return os.path.abspath(os.path.join(path, name))


_path = os.path.join(_base, 'conf', 'config.yml')
cfg = Cfg.from_yml(_path)
_path = os.path.join(_base, 'conf', 'logging.yml')
_log = Cfg._from_yml(_path)
_path = os.path.join(cfg.logdir, cfg.logname)
_log['handlers']['file']['filename'] = _path
logging.config.dictConfig(_log)

from .core import (Data, Isotopes, Constants, Units, Container, Editor,
                   DataFrame, Series, Field3D, Field, SparseDataFrame)
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
