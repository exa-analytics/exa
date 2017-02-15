# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
##################################
Tests that default abstract and concrete data objects behave like their `pandas`_
counterpart(s) and are interoperable with the rest of the `pydata`_ stack.

.. _pandas: http://pandas.pydata.org/
.. _pydata: http://pydata.org/
"""
import numpy as np
from exa.tester import UnitTester
#from exa.core.data import ABCData


# single valued 1d data
sv1d = {'feature0': np.random.rand(5)}
#sv2d =

class TestData(UnitTester):
    """Tests for :mod:`~exa.core.data`."""
    def setUp(self):
        pass


    def test_mixin(self):
        """Tests that :class:`~exa.core.data.ABCData` is abstract."""
        pass
#        with self.assertRaises(TypeError):
#            ABCData()
