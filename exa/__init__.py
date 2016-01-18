# -*- coding: utf-8 -*-
'''
exa
==============
This package provides the core functionality required for the
'''
import sys as _sys
import re as _re
import os as _os
import atexit as _ae
import numpy as _np
import pandas as _pd
import scipy as _sp
import seaborn as _sns
import json as _json


_sns.set_context('poster', font_scale=1.3)
_sns.set_palette('colorblind')
_sns.set_style('white')


__exa_version__ = (0, 1, 0)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))


from exa.utils import mkpath
from exa.config import Config
_ae.register(Config.save)
from exa.log import log_tail, log_head, setup
setup()
from exa.testers import run_unittests, run_doctests
from exa.dataframe import DataFrame
from exa.relational import Container
from exa.dashboard import Dashboard
_ae.register(relational.cleanup_anon_sessions)
_ae.register(relational.commit)
from exa import tests


# API cleanup
del setup, config, testers, log, dashboard, utils
try:
    del widget
except:
    pass
