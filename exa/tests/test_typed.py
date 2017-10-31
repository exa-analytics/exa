# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Strong Typing
########################
See :mod:`~exa.typed`
"""
import six
import pytest
from itertools import product
from exa.typed import Typed, typed, TypedClass, TypedMeta


@typed
class Simple1(object):
    foo = Typed(int)

    def __init__(self, foo):
        self.foo = foo


class Simple2(TypedClass):
    foo = Typed(int)

    def __init__(self, foo):
        self.foo = foo


class Simple3(six.with_metaclass(TypedMeta, Simple1)):
    pass


# params makes it so we test all the classes listed
params = list(product([Simple1, Simple2, Simple3],
                      [42, 42.0]))
@pytest.fixture(scope="session", params=params)
def simple(request):
    cls = request.param[0]
    arg = request.param[1]
    return cls(arg)


def test_simple(simple):
    """Test trivial typing."""
    assert isinstance(simple.foo, int)
    with pytest.raises(TypeError):
        simple.foo = "forty two"
    del simple._foo
    assert simple.foo is None


# Complex example
def pre_set(obj):
    obj.pre_set_called = True


class Complete(TypedClass):
    """Test advanced usage."""
    foo = Typed(int, doc="Test documentation", autoconv=False, allow_none=False,
                pre_set=pre_set)

    def __init__(self):
        self.pre_set_called = False


@pytest.fixture(scope="session")
def cmplx():
    return Complete()


def test_complex(cmplx):
    """Test auxiliary options of Typed attributes."""
    assert cmplx.pre_set_called == False
    cmplx.foo = 42
    assert cmplx.pre_set_called == True
