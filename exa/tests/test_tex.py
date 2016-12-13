# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.tex`
#############################################
Tests for LaTeX support.
"""
import numpy as np
import pandas as pd
from exa.tester import UnitTester
from exa.tex import cleanup_pandas


class TestTeX(UnitTester):
    """Tests for TeX support functions."""
    def test_cleanup_pandas(self):
        """Test :func:`~exa.tex.cleanup_pandas`."""
        df = pd.DataFrame(np.random.rand(3, 3))
        df.columns = ["$T_\mathrm{iso}$", "$T^{iso}$", "$\frac{1}{2}$"]
        string = df.to_latex()
        self.assertTrue("textbackslash" in string)
        self.assertTrue("textasciicircum" in string)
        string = cleanup_pandas(df.to_latex())
        self.assertFalse("textbackslash" in string)
        self.assertFalse("textasciicircum" in string)
