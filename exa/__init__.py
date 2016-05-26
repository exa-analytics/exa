# -*- coding: utf-8 -*-
__exa_version__ = (0, 2, 2)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))


import atexit as _ae


from exa._config import _conf, show_conf
from exa.log import log_names, log_head, log_tail
from exa.test import run_doctests, run_unittests
from exa import tests
from exa.relational.container import Container
from exa.symbolic import Symbolic
from exa.numerical import Series, DataFrame, Field3D, SparseDataFrame
from exa.editor import Editor
from exa import algorithms


if not _conf['exa_persistent']:
    from exa._install import install
    install()


if _conf['notebook']:
    i = get_ipython()
    c = i.config
    c.InteractiveShellApp.matplotlib = 'inline'


_ae.register(_config._cleanup)          # Register functions in opposite desired
_ae.register(log._cleanup)              # run order, first-in-last-out "FILO"
_ae.register(relational.base._cleanup)
