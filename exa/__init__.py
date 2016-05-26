# -*- coding: utf-8 -*-
__exa_version__ = (0, 2, 2)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))


# Setup up configuration, logging, testing
import atexit as _ae
from exa._config import _conf
from exa._install import install
from exa.log import logfiles, log_head, log_tail
from exa.test import run_doctests, run_unittests
syslog = log.get_logger('sys')
syslog.info('Starting exa with configuration:')
syslog.info(str(_conf))


# Import the container and trait supporting dataframe and series objects
from exa.relational.container import Container
from exa.numerical import Series, DataFrame
from exa.symbolic import Symbolic
from exa.editor import Editor

# Import sub-packages
from exa import algorithms

# Import tests
from exa import tests


# If dynamic (not persistent) session need to populate database tables
if not _conf['exa_persistent']:
    from exa.relational.base import setup_db
    from exa._install import install
    setup_db()
    install()


# If running in a Jupyter notebook set some reasonable defaults
if _conf['notebook']:
    i = get_ipython()
    c = i.config
    c.InteractiveShellApp.matplotlib = 'inline'


# Register cleanup functions
_ae.register(_config._cleanup)          # Register functions in opposite desired
_ae.register(log._cleanup)              # run order, first-in-last-out "FILO"
_ae.register(relational.base._cleanup)
