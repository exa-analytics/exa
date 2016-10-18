# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.project`
#############################################
"""
from exa.tester import UnitTester
from exa.cms.base import session_factory, engine
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
        self.conn = engine.connect()
        self.trans = self.conn.begin()
        self.session = session_factory(bind=self.conn)
        self.job.files.append(self.file0)
        self.project.files.append(self.file1)
        self.project.jobs.append(self.job)
        self.session.add(self.project)
        self.session.commit()

    def test_committed(self):
        """Test that the pkids exist."""
        pass

    def tearDown(self):
        """Clean up the table by rolling back the changes."""
        self.session.close()
        self.trans.rollback()
        self.conn.close()
