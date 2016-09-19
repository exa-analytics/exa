# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.mpl`
#############################################
"""
import numpy as np
from exa.mpl import color_palette
from exa.tester import UnitTester


class TestMPL(UnitTester):
    """
    """
    def test_color_palette(self):
        self.assertTrue(np.isclose(0.622722, color_palette()[0][2]))
