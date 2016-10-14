# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.files`
#############################################
"""
from exa.tester import UnitTester
from exa.cms.files import File


class TestFiles(UnitTester):
    """
    Tests for :mod:`~exa.cms.files`
    """
    def test_file_creation(self):
        """Test that file objects can be created."""
        try:
            f = File()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(f, File)
