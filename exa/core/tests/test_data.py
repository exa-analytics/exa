# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#############################################
"""
import numpy as np
import pandas as pd
from uuid import UUID, uuid4
from unittest import TestCase
from exa.core import DataFrame


class TestData(TestCase):
    """Tests for advanced data objects in :mod:`~exa.core.data`."""
    def test_empty(self):
        """Test creation of empty frame object."""
        df = DataFrame()
        self.assertIsInstance(df.uid, UUID)

    def test_abcmeta_attrs(self):
        """Test attributes provided by the metaclass."""
        name = "name"
        meta = {"description": "description"}
        uid = uuid4()
        df = DataFrame(uid=uid)
        self.assertEqual(df.uid, uid)
        df = DataFrame(uid=uid, name=name)
        self.assertEqual(df.uid, uid)
        self.assertEqual(df.name, name)
        df = DataFrame(uid=uid, name=name, meta=meta)
        self.assertEqual(df.uid, uid)
        self.assertEqual(df.name, name)
        self.assertEqual(df.meta, meta)

    def test_interop(self):
        """Test dataframe interoperability and operations."""
        data = np.random.rand(4, 4)
        df0 = DataFrame(data)
        df1 = pd.DataFrame(data)
        #self.assertTrue(np.all(data_add == df0 + df1))
        #self.assertTrue(np.all(data_add == df1 + df0))
        #self.assertTrue(np.all(data_mul == df0*df1))
        #self.assertTrue(np.all(data_mul == df1*df0))
        #self.assertTrue(np.all(data_sub == df0 - df1))
        #self.assertTrue(np.all(data_sub == df1 - df0))
