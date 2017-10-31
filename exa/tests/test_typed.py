# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Strong Typing
########################
See :mod:`~exa.typed`
"""
import pytest
from exa.typed import Typed, typed


@typed
class Simple(object):
    foo = Typed(int)

    def __init__(self, foo):
        self.foo = foo


@pytest.fixture
def simple():
    return Simple(42)


def test_simple(simple):
    """Test trivial typing."""
    assert isinstance(simple, Simple)
    assert isinstance(simple.foo, int)
    with pytest.raises(TypeError):
        simple.foo = "forty two"
    del simple._foo
    assert simple.foo is None
