# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
from exa._config import config
from exa.tests import test_tester, test_errors
if int(config['logging']['level']) > 0:    # Only load if info/debug level
    from exa.tests import test_config
