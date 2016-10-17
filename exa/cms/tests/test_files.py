# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.files`
#############################################
"""
import os
from exa._config import config
from exa.tester import UnitTester
from exa.cms.base import session_factory
from exa.cms.files import File


class TestFiles(UnitTester):
    """Tests for :mod:`~exa.cms.files`."""
    def test_file_creation(self):
        """Test that file objects can be created."""
        try:
            f = File()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(f, File)

    def test_tutorial_exists(self):
        """Test to make sure the default tutorial exists."""
        try:
            fp = os.path.join(config['paths']['notebooks'], 'tutorial.ipynb')
        except Exception as e:
            self.fail(str(e))
        if not os.path.exists(fp):
            self.fail(str(FileNotFoundError("Missing tutorial.ipynb at {}".format(fp))))
        try:
            fp0 = File[1]
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(fp0.name, "tutorial")

    def test_file_entry_present(self):
        """Test to ensure that the tutorial is the first entry in the db."""
        try:
            fp0 = File[1]
        except Exception as e:
            self.fail(str(e))
        try:
            fp1 = session_factory().query(File).filter(File.uid == fp0.uid).one()
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(fp0.uid, fp1.uid)
