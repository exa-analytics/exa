# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.framed`
##################################
"""
from exa.tester import UnitTester
from exa.core.framed import FrameData


class TestData(UnitTester):
    """Tests for :mod:`~exa.core.data`."""
    def setUp(self):
        self.data = FrameData()


    def test_mixin(self):
        """Tests that :class:`~exa.core.data.ABCData` is abstract."""
        pass
