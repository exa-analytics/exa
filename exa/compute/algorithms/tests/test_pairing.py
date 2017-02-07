# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.algorithms.pairing`
########################################################
"""
#from exa.tester import UnitTester
#from exa.compute.algorithms.pairing import (cantor, invert_cantor, szudzik,
#                                            invert_szudzik, unordered,
#                                            invert_unordered)
#
#
#class TestPairing(UnitTester):
#    """Tests for various types of pairing functions."""
#    def test_cantor(self):
#        """
#        Test :func:`~exa.compute.algorithms.pairing.cantor` and
#        :func:`~exa.compute.algorithms.pairing.invert_cantor`.
#        """
#        self.assertEqual(cantor(52, 1), 1432)
#        self.assertEqual(invert_cantor(1432), (52, 1))
#
#    def test_szudzik(self):
#        """
#        Test :func:`~exa.compute.algorithms.pairing.szudzik` and
#        :func:`~exa.compute.algorithms.pairing.invert_szudzik`.
#        """
#        self.assertEqual(szudzik(1, 1), 3)
#        self.assertEqual(invert_szudzik(3), (1, 1))
#
#    def test_unordered(self):
#        """Test :func:`~exa.compute.algorithms.pairing.unordered`."""
#        self.assertEqual(unordered(1, 3), 13)
#        self.assertEqual(invert_unordered(13), (3, 1))
