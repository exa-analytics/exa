# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#############################################
"""
from uuid import UUID, uuid4
from unittest import TestCase
from exa.util import ncr2
from exa.core import Frame


def data_helper(obs=3, n=4):
    """
    Helper function that generates related, multi-featured, multi-dimensional
    data.

    Data mimics a collection of particles, observed at sequential times, that
    move in (discretely measured) scalar and vector fields.

    Args:
        obs (int): Number of observations (time steps)
        n (int): Number of particles

    Returns:
        data (tuple): See note below

    Note:
        Returned data is a tuple of frame objects.
        - obs: Observations frame
        - pos: Particle positions frame
        - dist: Particle distances frame
        - srf: Scalar field frame
        - vrf: Vector field frame
    """
    nsnap = 3
    npart = 4
    snapshots = exa.Frame(np.arange(1, nsnap+1), columns=['time'])
    snapshots.index.name = 'snapshot'
    pos = exa.Frame(np.random.rand(nsnap*npart, 3), columns=['x', 'y', 'z'])
    pos.index.name = "particle"
    pos['label'] = list(np.arange(1, npart+1))*nsnap
    pos['snapshot'] = [i for i in snapshots.index.values for j in range(npart)]
    dist = sp.spatial.distance.pdist(pos[['x', 'y', 'z']])
    idx = ncr2(pos.index.values)
    distances = exa.Frame({'particle0': idx[:, 0], 'particle1': idx[:, 1], 'distance': dist})
    # finally need field example
    raise NotImplementedError()


class TestData(TestCase):
    """
    Tests for the :class:`~exa.core.data.Frame` and :class:`~exa.core.data.Field`
    data objects.
    """
    def test_empty(self):
        """Test creation of empty frame object."""
        df = Frame()
        self.assertIsInstance(df.uid, UUID)

    def test_abcmeta_attrs(self):
        """Test attributes provided by the metaclass."""
        name = "name"
        meta = {"description": "description"}
        uid = uuid4()
        df = Frame(uid=uid)
        self.assertEqual(df.uid, uid)
        df = Frame(uid=uid, name=name)
        self.assertEqual(df.uid, uid)
        self.assertEqual(df.name, name)
        df = Frame(uid=uid, name=name, meta=meta)
        self.assertEqual(df.uid, uid)
        self.assertEqual(df.name, name)
        self.assertEqual(df.meta, meta)



