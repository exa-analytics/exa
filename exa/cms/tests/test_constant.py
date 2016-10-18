# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.constant`
##########################################
Tests for the table of physical constants.
"""
import numpy as np
from six import string_types
from exa.tester import UnitTester
from exa.cms.constant import Constant


class TestConstant(UnitTester):
    """Tests for :mod:`~exa.cms.constant`."""
    def test_getters(self):
        """Test features of :class:`~exa.cms.constant.Meta`."""
        self.assertTrue(np.isclose(Constant.get_by_symbol("G"), 6.67384e-11))
        self.assertTrue(np.isclose(Constant['hartree'], 4.35974434e-18))

    def test_repr(self):
        """Test the string repr of :class:`~exa.cms.constant.Constant`."""
        self.assertIsInstance(repr(Constant['NA']), string_types)
