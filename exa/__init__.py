# -*- coding: utf-8 -*-
__exa_version__ = (0, 2, 2)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))


# Setup up configuration, logging, testing
import atexit as _ae
from exa._config import config as global_config
from exa._install import install
from exa.log import log_head, log_tail
from exa.test import run_doctests, run_unittests
from exa import mpl, tex
syslog = log.get_logger('sys')
syslog.info('Starting exa with configuration:')
syslog.info(str(global_config))


# Import the container and trait supporting dataframe and series objects
from exa.relational import Container
from exa.numerical import Series, DataFrame
from exa.symbolic import Symbolic
from exa.editor import Editor

# Import sub-packages
from exa import algorithms
from exa import distributed
from exa import relational
from exa import filetypes

# Import tests
from exa import tests


# If dynamic (not persistent) session need to populate database tables
if global_config['exa_persistent'] == False:
    install(False)


# If running in a Jupyter notebook set some reasonable defaults
if global_config['notebook']:
    _ipy = get_ipython()
    _ipyconf = _ipy.config
    _ipyconf.InteractiveShellApp.matplotlib = 'inline'


# Run some dynamic commands
relational.isotope.init_mappers()

# Register cleanup functions
_ae.register(_config.cleanup)          # Register functions in opposite desired
_ae.register(log.cleanup)              # run order, first-in-last-out "FILO"
_ae.register(relational.base.cleanup)
