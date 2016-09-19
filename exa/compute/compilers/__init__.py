# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
# Decide what compiler to import based on what packages are installed
from exa._config import config
if config['dynamic']['numba'] == 'true':
    from exa.compute.compilers import nb
