# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.util`
#############################################
Basic checks that dynamic modules are created
"""
import numpy as np

import exa

def test_created():
    """Check that constants were created."""
    assert len(dir(exa.util.constants)) > 300
    assert hasattr(exa.util.constants, "Planck_constant") == True

def test_attrs():
    """Check attributes of constants."""
    assert hasattr(exa.util.constants.Planck_constant, "value")
    assert hasattr(exa.util.constants.Planck_constant, "units")
    assert hasattr(exa.util.constants.Planck_constant, "name")
    assert hasattr(exa.util.constants.Planck_constant, "error")

def test_created():
    """Check that elements and isotope objects were created."""
    iso = exa.Isotopes.data()
    for sym in iso['symbol'].unique():
        assert hasattr(exa.util.isotopes, sym)

def test_element():
    """Test element attributes."""
    assert exa.util.isotopes.H.Z == 1
    assert exa.util.isotopes.H.mass > 1.007
    assert exa.util.isotopes.H.radius > 0.6

def test_isotope():
    """Test isotope attributes."""
    assert exa.util.isotopes.H['1'].Z == 1
    assert exa.util.isotopes.H['1'].A == 1
    assert exa.util.isotopes.H['1'].mass > 1.007
    assert exa.util.isotopes.H['1'].radius > 0.6

#def test_count():
#    """Check that all unit types have been created."""
#    assert hasattr(exa.util.units, "Acceleration") == True
#    assert hasattr(exa.util.units, "Energy") == True
#    assert hasattr(exa.util.units, "Length") == True
#    assert hasattr(exa.util.units, "Time") == True
#    assert hasattr(exa.util.units, "Mass") == True
#
#def test_units():
#    """Check attribute values."""
#    assert np.isclose(exa.util.units.Energy['J'], 1.0)
#    assert np.isclose(exa.util.units.Length['au', 'Angstrom'], 0.52918)
#    assert np.isclose(exa.util.units.Length['Angstrom'], 1E-10)


