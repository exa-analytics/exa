# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.base`
#############################################
Tests to ensure correct initialization of the base table (metaclass) for all
relational tables. Many of the tests act on the :class:`~exa.cms.files.File`
table because it has a convenient column set.
"""
import pandas as pd
from six import string_types
from datetime import datetime
from exa import _config
from exa.tester import UnitTester
from exa.cms.files import File
from exa.cms.job import Job
from exa.cms.base import reconfigure_session_factory, session_factory, scoped_session


class TestBase(UnitTester):
    """Test the base model for database tables."""
    def setUp(self):
        """
        Test generation of a table entry (for later use), string repr, and
        size computation (:class:`~exa.cms.base.Size`).
        """
        self.conn = _config.engine.connect()
        self.trans = self.conn.begin()
        self.session = session_factory(bind=self.conn)
        self.file = self.session.query(File).get(1)
        self.job = Job(name="test")
        self.job.files.append(self.file)
        self.job.update_sizes()
        self.session.add(self.job)
        self.session.commit()
        self.assertIsInstance(repr(self.file), string_types)

    def test_session_factory_config(self):
        """
        Test that :func:`~exa.cms.base.reconfigure_session_factory` works and
        that the :attr:`~exa.cms.base.session_factory` attribute is correctly
        bound to the engine.
        """
        reconfigure_session_factory()
        session = session_factory()
        self.assertTrue(hasattr(_config, "engine") and _config.engine is not None)
        session.close()

    def test_scoped_session(self):
        """Test the :func:`~exa.cms.base.scoped_session` context manager."""
        with scoped_session() as session:
            n = session.query(File).count()
        self.assertTrue(n > 0)
        with self.assertRaises(AttributeError):
            with scoped_session() as session:
                session.query(File).filter(File.missingobj == "mia").one()

    def test_getters(self):
        """
        Test the default getters of :class:`~exa.cms.base.BaseMeta`,
        :func:`~exa.cms.base.BaseMeta.get_by_pkid`,
        :func:`~exa.cms.base.BaseMeta.get_by_name`, and
        :func:`~exa.cms.base.BaseMeta.get_by_uid`.
        """
        self.assertEqual(self.file.name, "exa_tutorial")
        self.assertTrue(len(File.get_by_name("exa_tutorial")) > 0)
        self.assertTrue(File.get_by_uid(File[1].uid).name, "exa_tutorial")
        self.assertTrue(len(File['exa_tutorial']) > 0)
        self.assertIsInstance(File[self.file.uid], File)
        with self.assertRaises(KeyError):
            File[-1]
        with self.assertRaises(KeyError):
            File['random_name_that_does_not_exist']

    def test_to_series(self):
        """
        Test :func:`~exa.cms.base.Base.to_series` and
        :func:`~exa.cms.base.Sha256UID.sha256_from_file`.
        """
        se = self.file.to_series()
        self.assertEqual(se['uid'], self.file.uid)

    def test_to_frame(self):
        """Test :func:`~exa.cms.base.BaseMeta.to_frame`."""
        df = File.to_frame()
        self.assertIsInstance(df, pd.DataFrame)

    def test_time(self):
        """Test methods of :class:`~exa.cms.base.Time`."""
        now = datetime.now()
        self.assertTrue(self.file.modified < now)
        self.file.update_modified()
        self.assertTrue((now - self.file.modified).total_seconds() < 1)

    def test_commit(self):
        """Test database commit."""
        self.session.add(self.file)
        self.session.commit()
        self.assertEqual(self.session.query(File).get(self.file.pkid).uid, self.file.uid)

    def tearDown(self):
        """Remove test entry from database."""
        self.session.close()
        self.trans.rollback()
        self.conn.close()
