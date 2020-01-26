# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#######################################
"""

import pytest

import exa


def test_data():
    d = exa.Data()
    assert d.data() is None


def test_isotopes():
    assert not exa.Isotopes().data().empty


def test_compare(isotopes):
    from exa.util import isotopes as orig
    orig = orig.as_df()
    df = isotopes.data()
    subset = ['symbol', 'Z', 'cov_radius',
              'van_radius', 'color']
    assert df[subset].equals(orig[subset])
