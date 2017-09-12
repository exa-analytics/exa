# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Physical Constants
#############################################
Physical constants are created by a singleton factory paradigm.
"""
#from unittest import TestCase
#from exa import constants
#
#
#class TestConstants(TestCase):
#    """Basic checks that constants have been created."""
#    def test_singleness(self):
#        """Test that constants have been created."""
#        obj0 = constants.Hartree_energy()
#        obj1 = constants.Hartree_energy()
#        self.assertIs(obj0, obj1)
#        self.assertEqual(id(obj0), id(obj1))
#        self.assertIs(obj0.__dict__, obj1.__dict__)
#
#    def test_correct_values(self):
#        """Test that values have been correctly created."""
#        self.assertAlmostEqual(constants.standard_state_pressure.value, 100000)
