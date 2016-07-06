# -*- coding: utf-8 -*-
'''
exa
#########
This package creates a systematic infrastructure for an ecosystem of packages,
tailored to specific industry or academic displines, for organizing, processing,
analyzing, and visualizing data. It is built with minimal dependencies, leverages
established open-source packages, is itself extensible, and is targeted at both
industry and academic applications.

At a high level, data objects such as series or dataframes (i.e. `pandas`_
like objects) are organized into containers which track relationships between
these objects and provide methods for computation, conversion to other formats,
analysis, and visualization within the `Jupyter notebook`_ environment.

.. _pandas: http://pandas.pydata.org/pandas-docs/stable/index.html
.. _Jupyter notebook: http://jupyter.org/
'''
__exa_version__ = (0, 2, 3)
__version__ = '.'.join((str(v) for v in __exa_version__))


from exa import _setup

#from exa import _install
#from exa import log

#from exa import log
#from exa import _config
#_config.update_config()
#from exa import log
#log.setup_loggers()
#syslog = log.get_logger('sys')
#syslog.info('Starting exa with configuration:')
#syslog.info(str(_config.config))

# User API
#from exa.relational import Container
#from exa.numerical import Series, DataFrame
#from exa.symbolic import Symbolic
#from exa.editor import Editor
#from exa.filetypes import CSV
#
## Other API
#from exa import test, _install, tests
#
## Finalize config and cleanup
#if _config.config['exa_persistent'] == False:
#    _install.install()
#
#if _config.config['notebook']:
#    _ipy = get_ipython()
#    _ipyconf = _ipy.config
#    _ipyconf.InteractiveShellApp.matplotlib = 'inline'
#
#_ae.register(_config.cleanup)          # Register functions in opposite desired
#_ae.register(log.cleanup)              # run order, first-in-last-out "FILO"
#_ae.register(relational.base.cleanup_db)
#
