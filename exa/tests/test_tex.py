# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.tex`
#############################################
Tests for text manipulation functions.
"""
import re
import numpy as np
import pandas as pd
from unittest import TestCase
from exa import tex


class TestTeX(TestCase):
    """Test that modification of module level variables works."""
    def setUp(self):
        self.df = pd.DataFrame(np.random.rand(3, 3))
        self.df = self.df.astype(float)
        self.df.columns = ["$T_\mathrm{iso}$", "$T^{iso}$", "$\frac{1}{2}$"]
        self.badtext = self.df.to_latex()

    def test_cleanup_pandas(self):
        """Test :func:`~exa.tex.cleanup_pandas`."""
        self.assertTrue("textbackslash" in self.badtext)
        self.assertTrue("textasciicircum" in self.badtext)
        goodtext = tex.cleanup_pandas(self.badtext)
        self.assertFalse("textbackslash" in goodtext)
        self.assertFalse("textasciicircum" in goodtext)

    def test_mod_cleanup(self):
        """Test modification of :attr:`~exa.tex.cleaners` works."""
        tex.cleaners.append(("iso", "tropic"))
        self.assertTrue("iso" in self.badtext)
        goodtext = tex.cleanup_pandas(self.badtext)
        self.assertFalse("iso" in goodtext)

    def test_constant_decimals(self):
        """Test :func:`~exa.tex.constant_decimals`."""
        regex = "\.\d{1,}"
        # Test too few decimals
        text = tex.constant_decimals(self.df.round(2).to_latex(), 3)
        self.assertTrue(all(len(item) == 4 for item in re.findall(regex, text)))
        # Too many
        text = tex.constant_decimals(self.df.round(4).to_latex(), 3)
        self.assertTrue(all(len(item) == 4 for item in re.findall(regex, text)))

    def test_text_value_cleaner(self):
        """Test :func:`~exa.tex.text_value_cleaner(text)`."""
        flt = "  -10.1E1"
        res = tex.text_value_cleaner(flt)
        self.assertIsInstance(res, float)
        self.assertEqual(res, -101)
        num = " 42    "
        res = tex.text_value_cleaner(num)
        self.assertIsInstance(res, int)
        self.assertEqual(res, 42)
        fallback = " forty two "
        res = tex.text_value_cleaner(fallback)
        self.assertIsInstance(res, str)
        self.assertEqual(res, "forty two")
