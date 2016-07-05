# -*- coding: utf-8 -*-
__exa_version__ = (0, 2, 3)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))


# Setup up configuration, logging, testing
import atexit as _ae
from exa import _config
_config.update_config()
from exa import log
log.setup_loggers()
syslog = log.get_logger('sys')
syslog.info('Starting exa with configuration:')
syslog.info(str(_config.config))

# User API
from exa.relational import Container
from exa.numerical import Series, DataFrame
from exa.symbolic import Symbolic
from exa.editor import Editor
from exa.filetypes import CSV

# Other API
from exa import test, _install, tests

# Finalize config and cleanup
if _config.config['exa_persistent'] == False:
    _install.install()

if _config.config['notebook']:
    _ipy = get_ipython()
    _ipyconf = _ipy.config
    _ipyconf.InteractiveShellApp.matplotlib = 'inline'

_ae.register(_config.cleanup)          # Register functions in opposite desired
_ae.register(log.cleanup)              # run order, first-in-last-out "FILO"
_ae.register(relational.base.cleanup_db)
