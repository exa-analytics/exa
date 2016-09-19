# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.csv`
#############################################
This module does not test he base :class:`~exa.core.editor` functionality,
rather it only tests methods provided by :class:`~exa.core.ssv.CSV`.
"""
import numpy as np
import pandas as pd
from exa.tester import UnitTester
from exa.core.ssv import CSV


class TestCSV(UnitTester):
    """
    Test the :class:`~exa.core.ssv.CSV` class and related functionality.
    """
    def setUp(self):
        """Generate csv data to test."""
        self.csv = CSV(pd.DataFrame(np.random.rand(10, 3),
                                    columns=['c1', 'c2', 'c3']).to_csv(index=None))
        self.tsv = CSV(pd.DataFrame(np.random.rand(10, 3),
                                    columns=['c1', 'c2', 'c3']).to_csv(index=None,
                                                                       sep=" ",
                                                                       quotechar=" ",
                                                                       quoting=0,
                                                                       escapechar=" "))
        self.nsv = CSV(pd.DataFrame(np.random.rand(10, 3)).to_csv(index=None, header=None))

    def test_base(self):
        """Test that the editor was created (read in) correctly."""
        self.assertEqual(len(self.csv), 11)
        self.assertEqual(len(self.nsv), 10)
        self.assertEqual(len(self.tsv), 11)

    def test_sniffer(self):
        """Test the known sniffers."""
        self.assertEqual(self.csv.delimiter, ",")
        self.assertEqual(self.tsv.delimiter, " ")
        self.assertEqual(self.nsv.delimiter, ",")
