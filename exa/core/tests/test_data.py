# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
#"""
#Tests for :mod:`~exa.core.data`
##############################################
#Test data objects' behavior.
#"""
#import os
#import pytest
#import warnings
#import numpy as np
#import pandas as pd
##import symengine as sge
#from uuid import uuid4
#from tempfile import mkdtemp
#from exa.core.data import (DataSeries, DataFrame, SparseDataSeries,
#                           SparseDataFrame, Index, Column)#, Field)
## Ignore perf warnings for testing
#warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)
#
#
## Some simple Param tests
#class FooSeries(DataSeries):
#    idx = Index()
#
#
#class FooSeries1(DataSeries):
#    idx = Index(auto=False)
#
#
#class FooMSeries(DataSeries):
#    idx0 = Index(level=0)
#    idx1 = Index(level=1)
#
#
#class FooFrame(DataFrame):
#    idx = Index()
#    a0 = Column(int, required=True, verbose=False)
#    b1 = Column((float, str))
#
#    @property
#    def _constructor(self):
#        return FooFrame
#
#
#class BarFrame(DataFrame):
#    idx0 = Index(int, level=0, verbose=False)
#    idx1 = Index(str, level=1, verbose=False)
#    a0 = Column(int, required=True, verbose=False)
#    b1 = Column((float, str))
#
#
#@pytest.fixture(params=[DataSeries, DataFrame, FooSeries])
#def series(request):
#    return request.param(np.random.rand(10))#, meta={'ans': 42})
#
#
#@pytest.fixture
#def foo():
#    return FooSeries(np.random.rand(10))
#
#
#@pytest.fixture
#def foom():
#    index = pd.MultiIndex.from_product([[0, 1, 2], ["green", "purple"]])
#    return FooMSeries(index=index)
#
#
#@pytest.fixture(params=[DataSeries, DataFrame, SparseDataSeries, SparseDataFrame])
#def data(request):
#    return request.param(np.random.rand(10))
#
##@pytest.fixture(params=[sy.symbols("x y z") sge.var("x y z")])
##def field(request):
##    x, y, z = request.param
##    func = 2*((2 - (x**2 + y**2)**0.5)**2 + z**2)    # Torus
#
#
#def test_meta(series):
#    """Check that meta exists."""
#    assert isinstance(series.meta, dict)
#    assert series.meta['ans'] == 42
#    with pytest.raises(TypeError):
#        series.meta = [42]
#
#
#def test_fooseries(foo):
#    assert foo.index.name == "idx"
#    foo *= 10
#    assert foo.index.name == "idx"
#    foo = foo.iloc[:2]
#    assert foo.index.name == "idx"
#    with pytest.raises(NameError):
#        FooSeries1()
#
#
#def test_foomseries(foom):
#    assert foom.index.names == ["idx0", "idx1"]
#    foom *= 10
#    assert foom.index.names == ["idx0", "idx1"]
#    foom = foom.iloc[:2]
#    assert foom.index.names == ["idx0", "idx1"]
#
#
#def test_hdf(data):
#    """Test reading and writing to HDF."""
#    path = os.path.join(mkdtemp(), uuid4().hex)
#    data.to_hdf(path, "test")
#    assert os.path.exists(path) == True
#    d = data.__class__.from_hdf(path, "test")
#    assert d.meta == data.meta
#    assert np.allclose(d.values, data.values) == True
#    os.remove(path)
