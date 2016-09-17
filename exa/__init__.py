# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This package creates a framework for data management, computation, and analytics
and visualization. It is built atop the Python data stack (for more info see
`PyData`_) utilizing the `Jupyter notebook`_ interface as a GUI. It is written
with extensibility in mind.
"""
# Import base modules
from exa import _version, _config, tester, errors, mpl, tex

# Import sub-packages
from exa import cms, dtr, prc, tests

# Import top level API
from exa._version import __version__
from exa._config import print_config
from exa.mpl import color_palette
from exa.cms.editors.editor import Editor
from exa.cms.editors.csv import CSV
