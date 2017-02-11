# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataobj`
#############################################
"""
#import six
#import pandas as pd
#from exa.tester import UnitTester
#from exa.core.dataobj import PandasDataObject
#
#
#class MockDataObject(PandasDataObject, pd.Series):
#    """Example data object class for arbitrary data container."""
#    @property
#    def _constructor(self):
#        """Class name is callable."""
#        return MockDataObject
#
#    def as_pandas(self):
#        """Convert to a pandas data representation."""
#        return pd.Series(self)
#
#
#
#class TestDataObject(UnitTester):
#    """Testing an abstract base class for instantiation error."""
#    def test_instance(self):
#        with self.assertRaises(TypeError):
#            DataObject()
