# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
from exa._config import config
from exa.compute.compilers.tests import test_wrapper
if config['dynamic']['numba'] == "true":
    from exa.compute.compilers.tests import test_nb
if config['dynamic']['cython'] == "true":
    from exa.compute.compilers.tests import test_cy
