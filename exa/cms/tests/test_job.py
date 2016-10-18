# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.job`
#############################################
"""
import os
from exa.tester import UnitTester
from exa.cms.base import scoped_session
from exa.cms.job import Job, job_file
from exa.cms.files import File


class TestJob(UnitTester):
    """Tests for :mod:`~exa.cms.job`."""
    def setUp(self):
        try:
            self.job = Job(name="test", uid="test_uid"*8)
        except Exception as e:
            self.fail(str(e))

    def test_files(self):
        """Test adding files."""
        self.assertIsInstance(self.job.files, list)
        with self.assertRaises(AttributeError):
            self.job.files.append(None)
        try:
            self.job.files.append(File(name="test", uid="test_uid"*8))
        except Exception as e:
            self.fail(str(e))

    def test_save(self):
        """Test saving related objects."""
        try:
            with scoped_session(expire_on_commit=False) as session:
                session.add(self.job)
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(self.job.pkid, int)
        try:
            f = File["test_uid"*8]
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(f, File)
        try:
            File.delete(f.pkid)
            Job.delete(j.pkid)
        except Exception as e:
            self.fail(str(e))
