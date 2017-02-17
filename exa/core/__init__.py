# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This sub-package contains high level data manipulation API.

- :mod:`~exa.core.editor`: Programmatic file manipulation
"""
# Import base modules
from exa.core import errors, base, editor, container, framec, framed

# Import sub-packages
from exa.core import tests

# Import user/dev API
from exa.core.editor import Editor, Sections, Section
from exa.core.framec import FrameContainer
from exa.core.framed import FrameData
