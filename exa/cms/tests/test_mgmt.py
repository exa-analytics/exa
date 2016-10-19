# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.mgmt`
#############################################
"""
import blaze as bz
import pandas as pd
from sqlalchemy.exc import IntegrityError
from exa.tester import UnitTester
from exa.cms.mgmt import tables, tail, init_db, init_tutorial, db


class TestMgmt(UnitTester):
    """Tests for :mod:`~exa.cms.mgmt`."""
    def test_init_db(self):
        """Test :func:`~exa.cms.mgmt.init_db`."""
        init_db()
        self.assertTrue(hasattr(db, "fields"))

    def test_init_tutorial(self):
        """Test :func:`~exa.cms.mgmt.init_tutorial`."""
        with self.assertRaises(IntegrityError):
            init_tutorial()    # UID unique constraint should fail, since tutorial exists

    def test_tables(self):
        """Test :func:`~exa.cms.mgmt.tables`."""
        tbls = tables()
        self.assertIsInstance(tbls, list)
        self.assertTrue(len(tbls) > 10)

    def test_tail(self):
        """Test :func:`~exa.cms.mgmt.tail`."""
        df = tail("constant", n=1, to_frame=True)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertIn("value", df)
        df = tail("length")
        self.assertIsInstance(df, bz.expr.collections.Tail)
        self.assertEqual(len(df), 10)
