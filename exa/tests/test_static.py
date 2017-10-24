# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.static`
#############################################
"""
import os
from unittest import TestCase
from exa import static


class TestDataDir(TestCase):
    """Test that the static data directory is correctly found."""
    def test_staticdir(self):
        self.assertTrue(os.path.isdir(static.staticdir()))

    def test_resource(self):
        self.assertTrue(os.path.exists(static.resource("units.json.bz2")))
