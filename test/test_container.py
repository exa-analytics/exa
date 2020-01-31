# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.container`
#######################################
"""
from exa import Container


def test_container_constructor():
    c = Container()
    assert isinstance(c, Container)
    assert hasattr(c, "name")
    assert hasattr(c, "description")
    assert hasattr(c, "meta")
