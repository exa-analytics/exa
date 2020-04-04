# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#######################################
"""
import sys

import pytest

import exa

try:
    import pyarrow
except ImportError:
    pass

pyar = pytest.mark.skipif(
    'pyarrow' not in sys.modules, reason='requires pyarrow'
)

@pytest.fixture(scope='module')
def box():
    i = pyarrow.int16()
    assert i is not None
    return exa.Box()

@pytest.fixture(scope='module')
def fullbox(isotopes, constants):
    return exa.Box(isotopes=isotopes,
                   constants=constants)

def test_box_simple(box):
    assert box

def test_box_full(fullbox):
    assert fullbox

def test_box_copy(fullbox):
    notcopy = exa.Box(isotopes=fullbox.isotopes,
                      constants=fullbox.constants)
    assert notcopy.isotopes.data() is fullbox.isotopes.data()
    assert notcopy.constants.data() is fullbox.constants.data()
    copy = fullbox.copy()
    assert not copy.isotopes.data() is fullbox.isotopes.data()
    assert not copy.constants.data() is fullbox.constants.data()

def test_box_info(fullbox):
    df = fullbox.info()
    assert df.index.name == 'name'

def test_box_network():
    d0 = exa.Data(name='foo', indexes=['a', 'b'], columns=['a', 'b', 'c', 'd'])
    d1 = exa.Data(name='bar', indexes=['b', 'c'], columns=['b', 'c', 'd', 'e'])
    box = exa.Box(foo=d0, bar=d1)
    g = box.network()
    assert g.nodes
    assert g.edges

def test_box_save_load(fullbox, tmpdir):
    d = tmpdir.mkdir('test_box_load')
    fullbox.save(directory=d)
    nbox = exa.Box()
    nbox.load(name=fullbox.hexuid, directory=d)
    assert not nbox.isotopes is fullbox.isotopes
    assert not nbox.constants is fullbox.constants
    assert nbox.isotopes.data().equals(fullbox.isotopes.data())
    assert nbox.constants.data().equals(fullbox.constants.data())
