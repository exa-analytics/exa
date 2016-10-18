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
        try:
            self.file = File(name="test", uid="test_uid"*8, ext="nul")
            self.conn = engine.connect()
            self.trans = self.conn.begin()
            self.session = session_factory(bind=self.conn)
            self.session.add(self.file)
            self.session.commit()
        except Exception as e:
            self.fail(str(e))

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
            f = self.session.query(File).get(self.file.pkid)
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(f.uid, self.file.uid)

    def tearDown(self):
        """Clean up."""
        try:
            self.session.close()
        except Exception as e:
            self.fail(str(e))
        finally:
            self.trans.rollback()
            self.conn.close()
