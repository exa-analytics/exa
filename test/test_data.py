# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#######################################
"""
import os
import sys

import pytest
import pandas as pd
from traitlets import TraitError

import exa
from exa.core.error import RequiredColumnError

try:
    import pyarrow
except ImportError:
    pass

pyar = pytest.mark.skipif(
    'pyarrow' not in sys.modules, reason='requires pyarrow'
)


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
    with pytest.raises(TraitError):
        data.source = ''

def test_new_data_call_params():
    d = exa.Data(call_args=['a', 'b'],
                 call_kws={'a': 'b'})
    assert d.call_args == ['a', 'b']
    assert d.call_kws == {'a': 'b'}
    assert d.data() is None
    fun = lambda *a, **kws: a
    d.source = fun
    assert d.data() == tuple(d.call_args)
    fun = lambda *a, **kws: kws
    d.source = fun
    assert d.data(cache=False) == d.call_kws

def test_new_data_df(isotopes):
    d = exa.Data(df=isotopes.data())
    assert isotopes.data().equals(d.data())
    assert d.data() is isotopes.data()

def test_data_setting_source(data):
    fun = lambda *a: a[0] if a else None
    data.source = fun
    data.call_args = ['a', 'b']
    assert data.data() == 'a'
    data.source = None

def test_data_slice(data):
    assert data.slice(None) is None

def test_data_groupby(data):
    df = pd.DataFrame.from_dict(
        {'a': [1, 2], 'b': [3, 4]}
    )
    data.data(df=df)
    data.indexes = []
    assert data.groupby() is None
    data.indexes = ['a']
    grps = data.groupby()
    assert grps.ngroups == 2
    data.indexes = ['a', 'b']
    grps = data.groupby()
    assert grps.ngroups == 2
    data.indexes = []
    df[['a', 'b']] = 1
    data.data(df=df)
    grps = data.groupby(columns=['a', 'b'])
    assert grps.ngroups == 1

def test_data_memory(data):
    data.data(cache=False)
    assert not data.memory()
    df = pd.DataFrame.from_dict(
        {'a': [1, 2], 'b': [3, 4]}
    )
    data.data(df=df)
    assert data.memory().sum()

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
    data.categories = {'a': str, 'b': int, 'c': int}
    df = data.data(df=df)
    assert df['a'].dtype == 'category'
    df['d'] = 1
    data.indexes = ['d']
    with pytest.raises(TraitError):
        data.data(df=df)
    data.indexes = []

def test_data_cardinal(data):
    data.cardinal = 'a'
    data.indexes = ['a', 'b']
    with pytest.raises(TraitError):
        data.cardinal = 'c'
    data.indexes = []

@pyar
def test_data_save(isotopes, tmpdir):
    d = tmpdir.mkdir('test_data_save')
    isotopes.save(directory=d)
    assert os.path.isfile(os.path.join(d, 'isotopes.yml'))
    assert os.path.isfile(os.path.join(d, 'isotopes.qet'))
    d = exa.Data(name='tmp_data')
    d.save()
    od = exa.cfg.savedir
    assert os.path.isfile(os.path.join(od, 'tmp_data.yml'))
    assert not os.path.isfile(os.path.join(od, 'data.qet'))
    os.unlink(os.path.join(od, 'tmp_data.yml'))

@pyar
def test_data_load(data):
    i = pyarrow.int16()
    assert i is not None
    d = exa.Data(name='isotopes')
    adir = exa.cfg.resource('isotopes.yml')
    d.load(directory=os.path.dirname(adir))

def test_from_yml(isotopes):
    d = exa.Data.from_yml(exa.cfg.resource('isotopes.yml'))
    df = d.data()
    assert df.index.name == 'isotope'
    assert df['symbol'].dtype == 'category'
    assert df['Z'].dtype == 'category'
    assert not df.columns.difference(d.columns).any()
    assert df.shape == isotopes.data().shape

def test_from_yml_fail(tmpdir):
    d = tmpdir.mkdir('test_from_yml_fail')
    f = d.join("cfg.yml")
    f.write("""\
name: test
source: os.path.isfile
""")
    dum = exa.Data.from_yml(f)
    # os.path.isfile requires an argument and throws
    with pytest.raises(TypeError):
        dum.data()
    f = d.join("oth.yml")
    f.write("""\
name: test
source: os.path.dne
""")
    with pytest.raises(TraitError):
        dum = exa.Data.from_yml(f)
    d = exa.Data()
    with pytest.raises(TraitError):
        d.source = 1

def test_read_csv(tmpdir):
    d = tmpdir.mkdir('test_read_csv')
    f = d.join("tmp.csv")
    f.write("""\
foo, bar
0, 1
2, 3
""")
    dum = exa.Data.read_csv(f)
    assert isinstance(dum, exa.Data)

def test_copy(data):
    data._data = None
    n = data.copy()
    assert id(n) != id(data)
    df = pd.DataFrame()
    n.data(df=df)
    nn = n.copy()
    assert id(nn) != id(n)

def test_isotopes():
    assert not exa.Isotopes.data().empty

def test_constants():
    assert not exa.Constants.data().empty

def test_units():
    assert not exa.core.data.Units.data().empty
