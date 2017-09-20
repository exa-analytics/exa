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
from sys import getsizeof
from uuid import uuid4
from tempfile import mkdtemp
from unittest import TestCase
from exa.container import Container


class TestContainer(TestCase):
    def setUp(self):
        """Generate a test file."""
        self.dirpath = mkdtemp()
        self.path = os.path.join(self.dirpath, uuid4().hex)
        kwargs = {'a': "string", 'b': 42, 'c': 1.0, 'd': complex(42, 42),
                  'e': np.random.rand(10), 'f': np.random.rand(10, 3),
                  'g': pd.Series(np.random.rand(10)),
                  'h': pd.DataFrame(np.random.rand(10, 3)),
                  'i': pd.SparseSeries(np.random.rand(10)),
                  'j': pd.SparseDataFrame(np.random.rand(10, 3))}
        self.kwargs = kwargs
        self.c = Container(**kwargs)

    def test_hdf(self):
        """Test saving to and loading from HDF."""
        self.c.to_hdf(self.path)
        c = Container.from_hdf(self.path)
        self.assertEqual(c.a, self.c.a)
        self.assertEqual(c, self.c)
        os.remove(self.path)
        shutil.rmtree(self.dirpath)

    def test_info(self):
        """Test the information method works."""
        inf = self.c.info()
        self.assertEqual(len(inf), len(self.kwargs) + 2)    # 2 for the two typed attrs

    def test_memory_usage(self):
        """Test memory usage estimation."""
        self.assertTrue(np.isclose(self.c.memory_usage(), self.c.info()['size (MiB)'].sum()))
        size = self.c.info()['size (MiB)']*1024**2
        size = int(size.apply(np.ceil).sum())
        self.assertTrue(np.isclose(getsizeof(self.c), size, atol=10, rtol=100))

    def test_del(self):
        """Test item deletion."""
        del self.c['a']
        self.assertFalse(hasattr(self.c, "a"))
        self.c.a = self.kwargs['a']

    def test_len(self):
        """Test length check."""
        self.assertEqual(len(self.c), len(self.kwargs) + 2)

    def test_repr(self):
        """Test default container repr."""
        string = repr(self.c)
        self.assertIn(self.c.__class__.__name__, string)

    def test_arg_objs(self):
        """Test that args are created correctly."""
        c = Container("arg", 42)
        self.assertEqual(len(c), 4)
        self.assertEqual(len([arg for arg in c._items() if "obj_" in arg[0]]), 2)

    def test_network(self):
        """Test that we correctly get nodes and edges."""
        a = pd.DataFrame.from_dict({'size': [3]*3})
        a.index.name = "adx"
        b = pd.DataFrame.from_dict({'x': np.random.rand(9), 'adx': [i for i in range(3) for _ in range(3)]})
        b.index.name = "bdx"
        d = pd.DataFrame.from_dict({'y': np.random.rand(36), 'bdx': [i for i in range(9) for _ in range(4)]})
        e = pd.DataFrame(np.random.rand(10))
        c = Container(a=a, b=b, d=d, e=e)
        nodes, edges = c._network()
        self.assertListEqual(nodes, ["a", "b", "d", "e"])
        self.assertListEqual(edges, [["a", "b"], ["b", "d"]])
