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
import blaze as _bz
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
_idx = _pd.IndexSlice


from exa.config import Config
from exa.log import log_tail, log_head, setup
setup()
from exa.testers import run_unittests, run_doctests
from exa.tools import install_notebook_widgets



# relational
#from exa.relational import (Project, Job, File, Isotope, Length, Mass, Time,
#                            Temperature, Energy, Amount, MolarMass, Current,
#                            Luminosity, Dose, Acceleration, Angle, Charge,
#                            Dipole, Force, Frequency, Constant, end_session)
#_ae.register(end_session)
# unit and doc tests
#from exa.testers import run_unittests, run_doctests, UnitTester
#if Config.developer:
#    run_unittests(write_to_log=True)
#    run_doctests(write_to_log=True)
#    _ae.register(run_unittests, **{'write_to_log': True})
#    _ae.register(run_doctests, **{'write_to_log': True})
#from exa import tests

#from exa.widget import Widget

# API cleanup and version print
del setup, config, testers,
#print(__version__)
