# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa provides a custom notebook application and parallel execution environment.
"""
# Import base modules
from exa.app import main, notebook

# Import sub-packages
from exa.app import tests

# Import user/dev API
from exa.app.main import ExaApp
from exa.app.notebook import ExaNotebook
