# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.container`
#############################################
"""
import numpy as np
import pandas as pd
from uuid import UUID, uuid4
from unittest import TestCase
from exa.core import Container


class TestContainer(TestCase):
    """
    Test the container's data identification, categorization, and other
    functionality behavior.
    """
    def test_basic(self):
        """Test an empty container."""
        c = Container()
        self.assertIsInstance(c.uid, UUID)
        name = "name"
        meta = {"description": "description"}
        uid = uuid4()
        c = Container(uid=uid)
        self.assertEqual(c.uid, uid)
        c = Container(uid=uid, name=name)
        self.assertEqual(c.uid, uid)
        self.assertEqual(c.name, name)
        c = Container(uid=uid, name=name, meta=meta)
        self.assertEqual(c.uid, uid)
        self.assertEqual(c.name, name)
        self.assertEqual(c.meta, meta)

    def test_with_generic_data(self):
        """Test a container with normal data."""
        array = np.arange(10)
        series = pd.Series(array)
        df = pd.DataFrame.from_dict({'f': array, 'r': array[::-1]})
        c = Container(scalar=1, array=array, series=series, df=df, misc=["data"])
        self.assertEqual(len(c._data()), 5)
