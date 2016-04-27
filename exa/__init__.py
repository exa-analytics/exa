# -*- coding: utf-8 -*-
__exa_version__ = (0, 2, 1)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))

import atexit as _ae

# Sensible plotting defaults
import seaborn as _sns
_legend = {'legend.frameon': True, 'legend.facecolor': 'white',
           'legend.edgecolor': 'black'}
_mathtext = {'mathtext.default': 'rm'}
_save = {'savefig.format': 'pdf', 'savefig.bbox': 'tight',
         'savefig.transparent': True, 'savefig.pad_inches': 0.1,
         'pdf.compression': 9}
_rc = _legend
_rc.update(_mathtext)
_rc.update(_save)
_sns.set(context='poster', style='white', palette='colorblind', font_scale=1.3,
         font='serif', rc=_rc)

from exa._config import _conf, show_conf
from exa.utility import savefig
from exa.log import log_names, log_head, log_tail
from exa.test import run_doctests, run_unittests
from exa import tests
from exa.relational.container import Container
from exa.numerical import Series, DataFrame, Field3D, SparseDataFrame
from exa.editor import Editor
from exa import algorithms

if not _conf['exa_persistent']:
    from exa._install import install
    install()


_ae.register(_config._cleanup)          # Register functions in opposite desired
_ae.register(log._cleanup)              # run order, first-in-last-out "FILO"
_ae.register(relational.base._cleanup)
