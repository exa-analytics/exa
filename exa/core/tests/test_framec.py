# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.framec`
##################################
TODO
"""
from exa.tester import UnitTester
from exa.core.framec import FrameContainer


class TestData(UnitTester):
    """Tests for :mod:`~exa.core.framec`."""
    def setUp(self):
        self.container = FrameContainer()
