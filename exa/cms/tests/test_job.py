# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.job`
#############################################
"""
from exa.tester import UnitTester
from exa.cms.base import session_factory, engine
from exa.cms.job import Job, job_file
from exa.cms.files import File
from exa.cms.mgmt import tail


class TestJob(UnitTester):
    """Tests for :mod:`~exa.cms.job`."""
    def setUp(self):
        try:
            self.job = Job(name="test", uid="test_uid"*8)
            self.file = File(name="test", uid="test_uid"*8, ext="nul")
            self.conn = engine.connect()
            self.trans = self.conn.begin()
            self.session = session_factory(bind=self.conn)
            self.job.files.append(self.file)
            self.session.add(self.job)
            self.session.commit()
        except Exception as e:
            self.fail(str(e))

    def test_committed(self):
        """Test that pkids exist."""
        self.assertIsInstance(self.file.pkid, int)
        self.assertIsInstance(self.job.pkid, int)

    def test_files(self):
        """Test adding non-file objects."""
        self.assertIsInstance(self.job.files, list)
        with self.assertRaises(AttributeError):
            self.job.files.append("")

    def test_relationship(self):
        """Test that relationships were correctly created."""
        try:
            f = self.session.query(File).get(self.file.pkid)
            j = self.session.query(Job).get(self.job.pkid)
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(f, File)
        self.assertEqual(len(f.jobs), 1)
        self.assertEqual(len(j.files), 1)

    def tearDown(self):
        """Clean up inserted entries."""
        try:
            self.session.close()
        except Exception as e:
            self.fail(str(e))
        finally:
            self.trans.rollback()
            self.conn.close()
