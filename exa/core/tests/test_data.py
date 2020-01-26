# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#######################################
"""

import pytest
import numpy as np

import exa


def test_data():
    d = exa.Data()
    assert d.data() is None

def test_isotopes():
    assert not exa.Isotopes().data().empty

def test_constants():
    assert not exa.Constants().data().empty

def test_compare_isotopes(isotopes):
    from exa.util import isotopes as orig
    orig = orig.as_df()
    df = isotopes.data()
    subset = ['symbol', 'Z', 'cov_radius',
              'van_radius', 'color']
    assert df[subset].equals(orig[subset])

def test_compare_constants(constants):
    from exa.util import constants as con
    orig = con.as_df()
    df = constants.data()
    # Data issue in the old implementation
    # so fix new one to match for test
    df = df.drop_duplicates(
        subset=['name'], keep='last'
    ).reset_index(drop=True)
    subset = ['name', 'units']
    assert df[subset].equals(orig[subset])
    subset = ['value', 'error']
    assert np.allclose(df[subset], orig[subset])
