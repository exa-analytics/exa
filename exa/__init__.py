# -*- coding: utf-8 -*-
'''
exa
==============
This package provides the core functionality required for the 
'''
# Imports
import sys
import re
import os
import atexit as _ae
import blaze as bz
import numpy as np
import pandas as pd
import scipy as sp
import seaborn as sns
import yaml
try:
    from yaml import CLoader as Loader    # Only available where
    from yaml import CDumper as Dumper    # libyaml is installed.
except:
    from yaml import Loader, Dumper


# Package settings
sns.set_context('poster', font_scale=1.3)
sns.set_palette('colorblind')
sns.set_style('white')


# Aliases
__exa_version__ = (0, 0, 0)    # exa VERSION NUMBER
__version__ = '.'.join((str(v) for v in __exa_version__))
_idx = pd.IndexSlice


# configuration
#from exa.config import Config
#_ae.register(Config.save)
# logging
#from exa.log import setup, get_logger
#setup()
#_logger = get_logger()
#_logger.info('====================\nSTARTING exa SESSION\n====================')
#_logger.info('exa version {0}'.format(__version__))
# extensions
#from exa.tools import install_extensions
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
#del setup, config, testers
#print(__version__)
