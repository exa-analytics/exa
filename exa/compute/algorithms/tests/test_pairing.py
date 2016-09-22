# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.algorithms.pairing`
########################################################
"""
from exa.tester import UnitTester
from exa.compute.algorithms.pairing import cantor, invert_cantor


class TestCantor(UnitTester):
    """
    """
    def test_cantor(self):
        """
        """
        self.assertEqual(cantor(52, 1), 1432)
        self.assertEqual(cantor(1, 52), 1432)
