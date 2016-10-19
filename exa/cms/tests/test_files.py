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
from exa.cms.base import session_factory, engine
from exa.cms.files import File


class TestFiles(UnitTester):
    """Tests for :mod:`~exa.cms.files`."""
    def setUp(self):
        """Create a test file entry."""
        self.file = File(name="test", uid="test_uid"*8, ext="nul")
        self.conn = engine.connect()
        self.trans = self.conn.begin()
        self.session = session_factory(bind=self.conn)
        self.session.add(self.file)
        self.session.commit()

    def test_raises_fnf(self):
        """Test that creation raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            File.from_path("random_name_that_does_not_exist")

    def test_tutorial_exists(self):
        """Test to make sure the default tutorial exists."""
        fp = os.path.join(config['paths']['notebooks'], 'tutorial.ipynb')
        if not os.path.exists(fp):
            self.fail(str(FileNotFoundError("Missing tutorial.ipynb at {}".format(fp))))
        fp0 = File[1]
        self.assertEqual(fp0.name, "tutorial")

    def test_file_entry_present(self):
        """Test to ensure that the tutorial is the first entry in the db."""
        f = self.session.query(File).get(self.file.pkid)
        self.assertEqual(f.uid, self.file.uid)

    def tearDown(self):
        """Clean up."""
        self.session.close()
        self.trans.rollback()
        self.conn.close()
