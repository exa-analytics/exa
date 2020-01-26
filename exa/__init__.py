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
_app.parse_command_line(sys.argv)
_base = os.path.dirname(__file__)
_path = os.path.join(_base, 'conf', 'config.py')
_app.load_config_file(_path)


class Base:
    """This base class provides a configured
    log property and access to configuration
    driven application settings without
    forcing subclasses to be run explicitly
    in the context of an application.
    """

    @property
    def log(self):
        name = '.'.join([
            self.__module__, self.__class__.__name__
        ])
        return logging.getLogger(name)

    def __init__(self, *args, **kws):
        kws.pop('config', None)
        super().__init__(
            *args, config=_app.config, **kws
        )


class Cfg(Base, Configurable):
    logdir = Unicode().tag(config=True)
    logname = Unicode().tag(config=True)

    @validate('logdir')
    def _validate_logdir(self, prop):
        logdir = prop['value']
        os.makedirs(logdir, exist_ok=True)
        return prop['value']

    @default('logdir')
    def _default_logdir(self):
        base = os.path.expanduser('~')
        return os.path.join(base, '.exa')


cfg = Cfg()
_path = os.path.join(_base, 'conf', 'logging.yml')
with open(_path, 'r') as f:
    _log = yaml.safe_load(f.read())
_path = os.path.join(cfg.logdir, cfg.logname)
_log['handlers']['file']['filename'] = _path
logging.config.dictConfig(_log)

from .core import Data

#from ._version import __version__
#from .core import (DataFrame, Series, Field3D, Field, Editor, Container,
#                   TypedMeta, SparseDataFrame)
#
