# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataobj`
#############################################
"""
import six
from exa.tester import UnitTester
from exa.core.dataobj import DataObject


class TestDataObject(UnitTester):
    """Testing an abstract base class for instantiation error."""
    def test_instance(self):
        with self.assertRaises(TypeError):
            DataObject()
