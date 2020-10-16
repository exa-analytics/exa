# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Conversion Units
######################################
"""
from exa.util import conversions, constants
import numpy as np

def test_attrs():
    assert hasattr(conversions.Ha2inv_m, "value")
    assert hasattr(conversions.Ha2inv_m, "units")
    assert hasattr(conversions.Ha2inv_m, "name")
    assert hasattr(conversions.Ha2inv_m, "error")

def test_values():
    # TODO: the ideal thing to do here would be to pull
    #       the most updated values from NIST and then
    #       compare to make sure that the conversion
    #       units are the same
    assert np.isclose(conversions.Ha2inv_m.value,
                      constants.hartree_inverse_meter_relationship.value)
    assert np.isclose(conversions.amu2u.value,
                      constants.electron_mass_in_u.value)
    assert np.isclose(conversions.inv_m2eV.value,
                      constants.inverse_meter_electron_volt_relationship.value)
