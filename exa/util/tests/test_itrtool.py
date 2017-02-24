# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.util.itrtool`
#############################################
"""
import numpy as np
from unittest import TestCase
from exa.util import ncr2


class TestItrtool(TestCase):
    """Tests for :mod:`~exa.util.itrtool`."""
    def test_ncr2(self):
        """Tests for :func:`~exa.util.itrtool.ncr2`."""
        result = ncr2(np.array([0, 1, 2], dtype=np.int64))
        self.assertTrue(np.all(result == np.array([[0, 1], [0, 2], [1, 2]],
                                                  dtype=np.int64)))
