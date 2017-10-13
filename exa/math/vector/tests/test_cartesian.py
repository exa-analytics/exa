# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.math.vector.cartesian`
############################################
"""
import numpy as np
import pandas as pd
from unittest import TestCase
from exa.math.vector.cartesian import magnitude_xyz, magnitude_xyz_squared


class TestCartesian(TestCase):
    def setUp(self):
        """Testing arrays."""
        self.xyz = pd.DataFrame(np.random.rand(3, 3))

    def test_mag(self):
        check = (self.xyz**2).sum(1)**0.5
        result = magnitude_xyz(self.xyz[0], self.xyz[1], self.xyz[2])
        self.assertTrue(np.allclose(check, result))

    def test_mag_sq(self):
        check = (self.xyz**2).sum(1)
        result = magnitude_xyz_squared(self.xyz[0], self.xyz[1], self.xyz[2])
        self.assertTrue(np.allclose(check, result))
