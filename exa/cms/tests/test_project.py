# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.project`
#############################################
"""
from exa import _config
from exa.tester import UnitTester
from exa.cms.base import session_factory
from exa.cms.files import File
from exa.cms.job import Job
from exa.cms.project import Project


class TestProject(UnitTester):
    """Tests for :mod:`~exa.cms.project`."""
    def setUp(self):
        """Set up the test job and test (related) file."""
        self.project = Project(name="test")
        self.job = Job(name="test")
        self.file0 = File(name="test", uid="test_uid"*8, ext="nul")
        self.file1 = File(name="test", uid="test_iid"*8, ext="nul")
        self.conn = _config.engine.connect()
        self.trans = self.conn.begin()
        self.session = session_factory(bind=self.conn)
        self.job.files.append(self.file0)
        self.project.files.append(self.file1)
        self.project.jobs.append(self.job)
        self.session.add(self.project)
        self.session.commit()

    def test_committed(self):
        """Test that the pkids exist."""
        self.assertIsInstance(self.job.pkid, int)
        self.assertIsInstance(self.file0.pkid, int)
        self.assertIsInstance(self.file1.pkid, int)
        self.assertIsInstance(self.project.pkid, int)

    def test_relationship(self):
        """
        Tests that relationships were created correctly.

        Note:
            This is where :class:`~exa.cms.project.project_job` and
            :class:`~exa.cms.project.project_file` are tested.
        """
        f0 = self.session.query(File).get(self.file0.pkid)
        f1 = self.session.query(File).get(self.file1.pkid)
        j = self.session.query(Job).get(self.job.pkid)
        p = self.session.query(Project).get(self.project.pkid)
        self.assertEqual(len(f0.jobs), 1)
        self.assertEqual(len(f0.projects), 0)
        self.assertEqual(len(f0.list_projects), 1)
        self.assertEqual(len(f1.jobs), 0)
        self.assertEqual(len(f1.projects), 1)
        self.assertEqual(len(j.files), 1)
        self.assertEqual(len(j.list_files), 1)
        self.assertEqual(len(j.projects), 1)
        self.assertEqual(len(p.files), 1)
        self.assertEqual(len(p.list_files), 2)
        self.assertEqual(len(p.jobs), 1)

    def tearDown(self):
        """Clean up the table by rolling back the changes."""
        self.session.close()
        self.trans.rollback()
        self.conn.close()
