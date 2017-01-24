# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
Test Exa's data object metaclass (:class:`~exa.core.base.Meta`) and the indexer
aliasing class (:class:`~exa.core.base.Aliases`).
"""
import six
from exa.tester import UnitTester
from exa.core.base import DataObject


class TestDataObject(UnitTester):
    """Testing an abstract base class for instantiation error."""
    def test_instance(self):
        with self.assertRaises(TypeError):
            DataObject()
