# -*- coding: utf-8 -*-
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


from exa.config import Config
_ae.register(Config.save)
from exa.log import log_tail, log_head, setup
setup()
from exa.testing import run_unittests, run_doctests
from exa.frame import DataFrame
from exa.relational import Container, Session
from exa.editor import Editor
_ae.register(relational.cleanup_sessions)
_ae.register(relational.commit)
if Config._temp:
    _ae.register(Config.cleanup)
    relational.create_all()
if Config.interactive:
    from exa.install import initialize_database
    initialize_database()


# API cleanup
#del config, log, Config, decorators, editor, frames, setup, testers
