# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This sub-package contains high level data manipulation API.

- :mod:`~exa.core.editor`: Programmatic file manipulation
- :mod:`~exa.core.dataobj`: Abstract base data object
- :mod:`~exa.core.dataseries`: Single valued n-dimensional array
- :mod:`~exa.core.dataframe`: Multiply valued n-dimensional array
"""
# Import base modules
from exa.core import editor

# Import sub-packages
from exa.core import tests, filetypes

# Import user/dev API
from exa.core.editor import Editor
