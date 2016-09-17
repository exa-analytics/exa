# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.editors.csv`
#############################################
This module does not test he base :class:`~exa.cms.editors.editor` functionality,
rather it only tests methods provided by :class:`~exa.cms.editors.csv.CSV`.
"""
import numpy as np
import pandas as pd
from exa._config import config
from exa.tester import UnitTester
from exa.cms.editors.csv import CSV


class TestCSV(UnitTester):
    """
    Test the :class:`~exa.cms.editors.csv.CSV` class and related functionality.
    """
    def setUp(self):
        """
        Generate csv data to test.
        """
        self.csv = CSV(pd.DataFrame(np.random.rand(10, 3)).to_csv(index=None))

    def test_base(self):
        """
        Test that the editor was created (read in) correctly.
        """
        self.assertEqual(len(self.csv), 11)
