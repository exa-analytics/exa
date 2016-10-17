# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.job`
#############################################
"""
import os
from exa._config import config
from exa.tester import UnitTester
from exa.cms.job import Job, job_file


class TestJob(UnitTester):
    """Tests for :mod:`~exa.cms.job`."""
    def test_create_job(self):
        try:
            job = Job(name="test", uid='testuid')
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(job.uid, "testuid")
