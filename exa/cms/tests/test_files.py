# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.files`
#############################################
"""
import os
from exa import _config
from exa.tester import UnitTester
from exa.cms.base import session_factory
from exa.cms.files import File


class TestFiles(UnitTester):
    """Tests for :mod:`~exa.cms.files`."""
    def setUp(self):
        """Create a test file entry."""
        self.file = File.from_path(__file__)
        self.conn = _config.engine.connect()
        self.trans = self.conn.begin()
        self.session = session_factory(bind=self.conn)
        self.session.add(self.file)
        self.session.commit()

    def test_raises_fnf(self):
        """Test that creation raises OSError."""
        with self.assertRaises(OSError):
            File.from_path("random_name_that_does_not_exist")

    def test_tutorial_exists(self):
        """Test to make sure the default tutorial exists."""
        fp = os.path.join(_config.config['paths']['notebooks'], 'exa_tutorial.ipynb')
        if not os.path.exists(fp):
            self.fail(str(OSError("Missing exa_tutorial.ipynb at {}".format(fp))))
        fp0 = File[1]
        self.assertEqual(fp0.name, "exa_tutorial")

    def test_file_entry_present(self):
        """Test to ensure that the tutorial is the first entry in the db."""
        f = self.session.query(File).get(self.file.pkid)
        self.assertEqual(f.uid, self.file.uid)

    def tearDown(self):
        """Clean up."""
        os.remove(self.file.path)
        self.session.close()
        self.trans.rollback()
        self.conn.close()
