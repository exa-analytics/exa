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
def box():
    return exa.core.box.Box()

@pytest.fixture(scope='module')
def fullbox(isotopes, constants):
    return exa.core.box.Box(isotopes=isotopes,
                            constants=constants)

def test_box_simple(box):
    assert box

def test_box_full(fullbox):
    assert fullbox

def test_box_copy(fullbox):
    notcopy = exa.core.box.Box(isotopes=fullbox.isotopes,
                               constants=fullbox.constants)
    assert notcopy.isotopes.data() is fullbox.isotopes.data()
    assert notcopy.constants.data() is fullbox.constants.data()
    copy = fullbox.copy()
    assert not copy.isotopes.data() is fullbox.isotopes.data()
    assert not copy.constants.data() is fullbox.constants.data()

def test_box_info(fullbox):
    df = fullbox.info()
    assert df.index.name == 'name'

def test_box_network(fullbox):
    g = fullbox.network()

def test_box_save(fullbox, tmpdir):
    d = tmpdir.mkdir('test_box_save')
    fullbox.save(directory=d)
