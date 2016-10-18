# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
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
from exa.tester import UnitTester
from exa.cms.files import File
from exa.cms.mgmt import tail
from exa.cms.base import (reconfigure_session_factory, session_factory,
                          scoped_session, engine)


class TestBase(UnitTester):
    """Test the base model for database tables."""
    def setUp(self):
        """Test generation of a table entry (for later use) and string repr."""
        try:
            self.fp = File.from_path(__file__)
            self.conn = engine.connect()
            self.trans = self.conn.begin()
            self.session = session_factory(bind=self.conn)
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(repr(self.fp), string_types)

    def test_session_factory_config(self):
        """
        Test that :func:`~exa.cms.base.reconfigure_session_factory` works and
        that the :attr:`~exa.cms.base.session_factory` attribute is correctly
        bound to the engine.
        """
        try:
            reconfigure_session_factory()
        except Exception as e:
            self.fail(str(e))
        try:
            session = session_factory()
            session.close()
        except Exception as e:
            self.fail(str(e))
        self.assertTrue(engine is session_factory.kw['bind'])

    def test_scoped_session(self):
        """Test the :func:`~exa.cms.base.scoped_session` context manager."""
        try:
            with scoped_session() as session:
                n = session.query(File).count()
            self.assertTrue(n > 0)
        except Exception as e:
            self.fail(str(e))
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
        try:
            tut = File.get_by_pkid(1)
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(tut.name, "tutorial")
        self.assertTrue(len(File.get_by_name("tutorial")) > 0)
        self.assertTrue(File.get_by_uid(File[1].uid).name, "tutorial")
        self.assertTrue(len(File['tutorial']) > 0)
        self.assertIsInstance(File[tut.uid], File)
        with self.assertRaises(KeyError):
            File[-1]

    def test_to_series(self):
        """
        Test :func:`~exa.cms.base.Base.to_series` and
        :func:`~exa.cms.base.Sha256UID.sha256_from_file`.
        """
        try:
            se = self.fp.to_series()
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(se['uid'], self.fp.uid)

    def test_to_frame(self):
        """Test :func:`~exa.cms.base.BaseMeta.to_frame`."""
        try:
            df = File.to_frame()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(df, pd.DataFrame)

    def test_time(self):
        """Test methods of :class:`~exa.cms.base.Time`."""
        now = datetime.now()
        self.assertTrue(self.fp.modified < now)
        self.fp.update_modified()
        self.assertTrue((now - self.fp.modified).total_seconds() < 1)

    def test_commit(self):
        """Test database commit."""
        try:
            self.session.add(self.fp)
            self.session.commit()
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(self.session.query(File).get(self.fp.pkid).uid, self.fp.uid)

    def tearDown(self):
        """Remove test entry from database."""
        try:
            self.session.close()
        except Exception as e:
            self.fail(str(e))
        finally:
            self.trans.rollback()
            self.conn.close()
