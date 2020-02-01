# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#######################################
"""

import pytest
import numpy as np
import pandas as pd

import exa
from exa.core.error import RequiredColumnError


@pytest.fixture(scope='module')
def data():
    return exa.Data()

def test_data_simple(data):
    assert data.data() is None
    fun = lambda: 42
    data.source = fun
    assert data.data() == 42
    data.source = None
    assert data.data() is None

def test_new_data_source_params():
    d = exa.Data(source_args=['a', 'b'],
                 source_kws={'a': 'b'})
    assert d.source_args == ['a', 'b']
    assert d.source_kws == {'a': 'b'}
    assert d.data() is None
    fun = lambda *a, **kws: a
    d.source = fun
    assert d.data() == tuple(d.source_args)
    fun = lambda *a, **kws: kws
    d.source = fun
    assert d.data(cache=False) == d.source_kws

def test_data_setting_source(data):
    fun = lambda *a: a[0] if a else None
    data.source = fun
    data.source_args = ['a', 'b']
    assert data.data() == 'a'
    data.source = None

def test_data_validation(data):
    df = pd.DataFrame.from_dict(
        {'a': [1, 2], 'b': [3, 4]}
    )
    data.data(df=df)
    assert data.data().equals(df)
    data.columns = ['c']
    with pytest.raises(RequiredColumnError):
        data.data(df=df)
    data.columns = []
    data.categories = {'a': str, 'b': int}
    df = data.data(df=df)
    assert df['a'].dtype == 'category'

def test_from_yml(isotopes):
    d = exa.Data.from_yml(exa.cfg.resource('isotopes.yml'))
    df = d.data()
    assert df.index.name == 'isotope'
    assert df['symbol'].dtype == 'category'
    assert df['Z'].dtype == 'category'
    assert not df.columns.difference(d.columns).any()
    assert df.shape == isotopes.data().shape

def test_isotopes():
    assert not exa.Isotopes.data().empty

def test_constants():
    assert not exa.Constants.data().empty

def test_units():
    assert not exa.core.data.Units.data().empty
