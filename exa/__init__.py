# -*- coding: utf-8 -*-
__exa_version__ = (0, 2, 0)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))


import atexit as _ae
import seaborn as _sns
_sns.set_context('poster', font_scale=1.3)    # This may override user plotting
_sns.set_palette('colorblind')                # defaults...
_sns.set_style('white')


from exa._config import _conf, show_conf
from exa.log import log_names, log_head, log_tail
from exa.test import run_doctests, run_unittests
from exa import tests
from exa import relational
from exa.container import Container
#from exa.editor import Editor
#from exa.container import Container


if _conf['exa_persistent']:
    pass    # Eventually do something here
else:
    from exa._install import install
    install()


_ae.register(_config._cleanup)          # Register functions in opposite desired
_ae.register(log._cleanup)              # run order, first-in-last-out "FILO"
_ae.register(relational.base._cleanup)
