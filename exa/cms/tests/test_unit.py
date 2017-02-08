# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.unit`
##########################################
"""
import numpy as np
from exa.tester import UnitTester
from exa.cms.base import scoped_session
from exa.cms.unit import (Length, Mass, Time, Current, Amount, Luminosity,
                          Dose, Acceleration, Charge, Dipole, Energy, Force,
                          Frequency, MolarMass)


class TestUnits(UnitTester):
    """
    Test different types of unit conversions available in classes such as
    :class:`~exa.cms.unit.Length` and similar.
    """
    def test_length(self):
        """Test :class:`~exa.cms.unit.Length`."""
        self.assertTrue(np.isclose(Length['angstroms', 'au'], 1.88971616463))
        self.assertTrue(np.isclose(Length['km', 'm'], 1000))

    def test_mass(self):
        """Test :class:`~exa.cms.unit.Mass`."""
        self.assertTrue(np.isclose(Mass['amu', 'kg'], 1.66053892e-27))
        self.assertTrue(np.isclose(Mass['kg', 'g'], 1000))

    def test_time(self):
        """Test :class:`~exa.cms.unit.Time`."""
        self.assertTrue(np.isclose(Time['min', 's'], 60))
        self.assertTrue(np.isclose(Time['weeks', 'days'], 7))

    def test_current(self):
        """Test :class:`~exa.cms.unit.Current`."""
        self.assertTrue(np.isclose(Current['A', 'C_s'], 1.0))
        self.assertTrue(np.isclose(Current['A', 'Bi'], 0.1))

    def test_amount(self):
        """Test :class:`~exa.cms.unit.Amount`."""
        self.assertTrue(np.isclose(Amount['gmol', 'mol'], 1.0))
        self.assertTrue(np.isclose(Amount['lbmol', 'mol'], 453.592374495))

    def test_luminosity(self):
        """Test :class:`~exa.cms.unit.Luminosity`."""
        self.assertTrue(np.isclose(Luminosity['cp', 'cd'], 0.981))

    def test_dose(self):
        """Test :class:`~exa.cms.unit.Dose`."""
        self.assertTrue(np.isclose(Dose['Gy', 'rd'], 100.0))
        self.assertTrue(np.isclose(Dose['J_kg', 'rd'], 100.0))

    def test_acceleration(self):
        """Test :class:`~exa.cms.unit.Acceleration`."""
        self.assertTrue(np.isclose(Acceleration['m_s2', 'cm_s2'], 100.0))
        self.assertTrue(np.isclose(Acceleration['m_s2', 'stdgrav'], 0.101971621))

    def test_charge(self):
        """Test :class:`~exa.cms.unit.Charge`."""
        self.assertTrue(np.isclose(Charge['e', 'C'], 1.602176565e-19))

    def test_dipole(self):
        """Test :class:`~exa.cms.unit.Dipole`."""
        self.assertTrue(np.isclose(Dipole['yCm', 'D'], 299792.45817809016))

    def test_energy(self):
        """Test :class:`~exa.cms.unit.Energy`."""
        self.assertTrue(np.isclose(Energy['J', 'cal'], 0.2388458966))
        self.assertTrue(np.isclose(Energy['cm-1', 'J'], 1.986314294511e-23))

    def test_force(self):
        """Test :class:`~exa.cms.unit.Force`."""
        self.assertTrue(np.isclose(Force['N', 'lbf'], 0.2248089431))

    def test_frequency(self):
        """Test :class:`~exa.cms.unit.Frequency`."""
        self.assertTrue(np.isclose(Frequency['1_s', 'Hz'], 1.0))

    def test_molarmass(self):
        """Test :class:`~exa.cms.unit.MolarMass`."""
        self.assertTrue(np.isclose(MolarMass['g_mol', 'kg_mol'], 0.001))

    def test_keyerror(self):
        """Test to ensure that proper error is raised on failed retrieval."""
        with self.assertRaises(KeyError):
            MolarMass["g_mol"]
