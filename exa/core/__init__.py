# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This sub-package contains the core functionality of exa:

- :class:`~exa.core.analytical`: Analytical data objects
- :class:`~exa.core.units`: Quantity support (data object with associated units)
- :class:`~exa.core.discrete`: Discrete data objects
- :class:`~exa.core.editor.Editor`: Programmatic file manipulation
- :class:`~exa.core.container.Container`: Data object analysis and visualization toolkit
"""
# Import base modules
from exa.core import editor, ssv, indexing, series

# Import sub-packages
from exa.core import tests

# Import user/dev API
from exa.core.editor import Editor
from exa.core.ssv import CSV
from exa.core.series import Series
