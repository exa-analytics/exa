# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.container`
#######################################
"""
import os
from tempfile import mkdtemp
from shutil import rmtree
from logging import Logger
import pandas as pd
from pytest import fixture
from exa import Container, DataFrame


@fixture(scope="module")
def c():
    df = DataFrame([[1, 4], [2, 5], [3, 6]],
                   columns=("i", "other")).set_index("i")
    derived = DataFrame([[4, 7], [5, 8]],
                        columns=("other", "another")).set_index("other")
    return Container(
        name="Name",
        df=df,
        derived=derived,
    )


def test_container_constructor(c):
    assert isinstance(c, Container)
    assert hasattr(c, "name")
    assert hasattr(c, "description")
    assert hasattr(c, "meta")


def test_container_copy(c):
    copy = c.copy()
    assert copy is not c
    assert copy.df is not c.df
    assert copy.derived is not c.derived
    assert copy.name == c.name
    assert copy.df.equals(c.df)
    assert copy.derived.equals(c.derived)


def test_container_slicing(c):
    sliced = c[:1]
    assert sliced.df is not c.df
    assert sliced.df.shape == (1, 1)
    assert sliced.name == c.name
    assert sliced.derived.shape == (1, 1)


def test_container_cardinal_slicing(c):
    c._cardinal = "df"
    sliced = c[[2]]
    assert sliced.df is not c.df
    assert sliced.df.shape == (1, 1)
    assert sliced.derived.shape == (1, 1)
    assert list(sliced.df.index) == [2]
    assert list(sliced.derived.index) == [5]


def test_container_logger(c):
    assert isinstance(c.log, Logger)


def test_network(c):
    g = c.network()
    assert sorted(g.nodes) == ["derived", "df"]
    assert sorted(g.edges) == [("derived", "df")]


def test_info(c):
    assert isinstance(c.info(), pd.DataFrame)
    assert c.info().shape == (4, 2)


def test_memory_usage(c):
    assert isinstance(c.memory_usage(), pd.Series)
    assert isinstance(c.memory_usage(True), str)


def test_save_load(c):
    dirpath = mkdtemp()
    path = c.save(dirpath)
    assert os.path.exists(path)
    c.to_hdf(path)
    assert os.path.exists(path)
    new = Container.load(path)
    assert hasattr(new, "df")
    assert hasattr(new, "derived")
    assert new.df.equals(c.df)
    assert new.derived.equals(c.derived)
    new = Container.from_hdf(path)
    assert isinstance(new, Container)
    rmtree(dirpath)


def test_data(c):
    d = c._data()
    assert c.df is d['df']
    assert c.derived is d['derived']
