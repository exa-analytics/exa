# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This sub-package contains the core functionality of exa:

- :class:`~exa.core.editor.Editor`
- :class:`~exa.core.container.Container`
"""
# Import base modules
from exa.core import typed, editor, ssv

# Import sub-packages
from exa.core import tests

# Import user/dev API
from exa.core.editor import Editor
from exa.core.ssv import CSV
