# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa
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
"""
from exa._version import __version__
from exa import _config
from exa import tester
from exa import relational
#from exa import widget
#from exa import math
#from exa import distributed
#from exa import mpl, tex
#from exa import error

# User API
#from exa.numerical import Series, DataFrame, Field3D, SparseSeries, SparseDataFrame
#from exa.container import Container
#from exa.editor import Editor
#from exa.filetypes import CSV

from exa import tests
