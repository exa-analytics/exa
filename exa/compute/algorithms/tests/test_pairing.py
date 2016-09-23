# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.algorithms.pairing`
########################################################
"""
from exa.tester import UnitTester
from exa.compute.algorithms.pairing import cantor, invert_cantor


class TestPairing(UnitTester):
    """Tests for various types of pairing functions."""
    def test_cantor(self):
        """
        Test :func:`~exa.compute.algorithms.pairing.cantor` and
        :func:`~exa.compute.algorithms.pairing.invert_cantor`.
        """
        self.assertEqual(cantor(52, 1), 1432)
        self.assertEqual(cantor(1, 52), 1483)
        self.assertEqual(invert_cantor(1432), (52, 1))
        self.assertEqual(invert_cantor(1483), (1, 52))
