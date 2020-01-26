# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa
#########
"""
import os
import sys
import logging.config

import yaml
from traitlets import Unicode, default, validate
from traitlets.config import Configurable, Application


_app = Application()
try:
    _app.parse_command_line(sys.argv)
except SystemExit:
    # _app fails to parse pytest command line
    # so just pass the failure in this case.
    pass
_base = os.path.abspath(os.path.dirname(__file__))
_path = os.path.join(_base, 'conf', 'config.py')
_app.load_config_file(_path)


class Base:
    """This base mixin class provides a configured
    log property and access to configuration
    driven application settings without
    forcing subclasses to be run explicitly
    in the context of an application. It expects
    to be mixed with a traitlets.config.Configurable
    """

    @property
    def log(self):
        name = '.'.join([
            self.__module__, self.__class__.__name__
        ])
        return logging.getLogger(name)

    def traits(self, *args, **kws):
        # inherent to traitlets API and
        # of little concern to us here.
        skipme = ['parent', 'config']
        traits = super().traits(*args, **kws)
        return {k: v for k, v in traits.items()
                if k not in skipme}

    def trait_items(self):
        return {k: getattr(self, k)
                for k in self.traits()}

    def __init__(self, *args, **kws):
        # Allow over-writing config for dynamic
        # classes at runtime
        config = kws.pop('config', _app.config)
        super().__init__(
            *args, config=config, **kws
        )


class Cfg(Base, Configurable):
    logdir = Unicode().tag(config=True)
    logname = Unicode().tag(config=True)
    staticdir = Unicode()

    @validate('logdir')
    def _validate_logdir(self, prop):
        logdir = prop['value']
        os.makedirs(logdir, exist_ok=True)
        return prop['value']

    @default('logdir')
    def _default_logdir(self):
        base = os.path.expanduser('~')
        return os.path.join(base, '.exa')

    @default('staticdir')
    def _default_staticdir(self):
        return os.path.join(_base, "static")

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


cfg = Cfg()
_path = os.path.join(_base, 'conf', 'logging.yml')
with open(_path, 'r') as f:
    _log = yaml.safe_load(f.read())
_path = os.path.join(cfg.logdir, cfg.logname)
_log['handlers']['file']['filename'] = _path
logging.config.dictConfig(_log)

from ._version import __version__
from .core import (DataFrame, Series, Field3D, Field, Editor, Container,
                   TypedMeta, SparseDataFrame)

from .core import Data, Isotopes, Constants

#
