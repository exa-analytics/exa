# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.container`
#############################################
Tests the behavior of the generic container.
"""
import os
import shutil
import numpy as np
import pandas as pd
from uuid import uuid4
from tempfile import mkdtemp
from unittest import TestCase
from exa.container import Container


class TestContainer(TestCase):
    def setUp(self):
        self.dirpath = mkdtemp()
        self.path = os.path.join(self.dirpath, uuid4().hex)
        kwargs = {'a': "string", 'b': 42, 'c': 1.0, 'd': complex(42, 42),
                  'e': np.random.rand(10), 'f': np.random.rand(10, 3),
                  'g': pd.Series(np.random.rand(10)),
                  'h': pd.DataFrame(np.random.rand(10, 3)),
                  'i': pd.SparseSeries(np.random.rand(10)),
                  'j': pd.SparseDataFrame(np.random.rand(10, 3))}
        self.c = Container(**kwargs)

    def test_hdf(self):
        """Test saving to and loading from HDF."""
        self.c.to_hdf(self.path)
        with pd.HDFStore(self.path) as store:
            self.assertIn("/__SPECIAL__", store.keys())
        c = Container.from_hdf(self.path)
        self.assertEqual(c.a, self.c.a)

    def tearDown(self):
        os.remove(self.path)
        shutil.rmtree(self.dirpath)
