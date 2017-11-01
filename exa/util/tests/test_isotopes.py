# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.isotopes`
#############################################
Note that elements and isotope singletons are created on module import.
"""
from exa.util import isotopes


def test_created():
    """Check that elements and isotope objects were created."""
    iso = isotopes.df
    for sym in iso['symbol'].unique():
        assert hasattr(isotopes, sym) == True


def test_element():
    """Test element attributes."""
    assert isotopes.H.Z == 1
    assert isotopes.H.mass > 1.007
    assert isotopes.H.radius > 0.6


def test_isotope():
    """Test isotope attributes."""
    assert isotopes.H[1].Z == 1
    assert isotopes.H[1].A == 1
    assert isotopes.H[1].mass > 1.007
    assert isotopes.H[1].radius > 0.6
