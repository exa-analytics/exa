# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.static`
#############################################
"""
import os
from exa import static


def test_static_dir():
    """Test :func:`~exa.static.staticdir`."""
    assert os.path.isdir(static.staticdir())


def test_resource():
    assert os.path.exists(static.resource("units.json.bz2"))
