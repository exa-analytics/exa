# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
from exa._config import config
from exa.tests import (test_tester, test_errors, test_mpl, test_typed, test_tex,
                       test_config)
#if int(config['logging']['level']) > 0:    # Only load if debug level logging
#    from exa.tests import test_config      # because this test is slow.
