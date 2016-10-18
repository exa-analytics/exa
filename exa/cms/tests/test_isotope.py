# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.isotope`
##########################################
Tests for the isotope table.
"""
import numpy as np
import pandas as pd
from six import string_types
from exa.tester import UnitTester
from exa.cms.isotope import (Isotope, Element, elements, symbol_to_znum,
                             znum_to_symbol, symbol_to_radius, symbol_to_mass,
                             symbol_to_color)


class TestIsotope(UnitTester):
    """
    Tests for :class:`~exa.cms.isotope.Isotope` and related mapping functions.
    """
    def test_get_by_strid(self):
        """Test :func:`~exa.cms.isotope.Meta.get_by_strid`."""
        try:
            isotope = Isotope["1H"]
        except Exception as e:
            self.fail(str(e))
        self.assertEqual(isotope.strid, "1H")

    def test_get_by_symbol(self):
        """Test :func:`~exa.cms.isotope.Meta.get_by_symbol`."""
        try:
            isotopes = Isotope["H"]
        except Exception as e:
            self.fail(str(e))
        self.assertTrue(len(isotopes) > 3)

    def test_default_getters(self):
        """Test remaining (default) getters."""
        try:
            isotope = Isotope[1]
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(isotope, Isotope)

    def test_compute_element(self):
        """
        Test :func:`~exa.cms.isotope.Isotope.element` and
        :func:`~exa.cms.isotope.Meta.compute_element`.
        """
        try:
            h = Isotope.element("H")
            hh = Isotope.element("hydrogen")
            o = Isotope.element("O")
            u = Isotope.element("uranium")
        except Exception as e:
            self.fail(str(e))
        self.assertTrue(np.isclose(h.mass, 1.0079105192))
        self.assertEqual(hh.name, "hydrogen")
        self.assertEqual(o.name, "oxygen")
        self.assertEqual(u.name, "uranium")

    def test_repr(self):
        """Test :class:`~exa.cms.isotope.Isotope` repr."""
        self.assertIsInstance(repr(Isotope['1H']), string_types)


class TestElement(UnitTester):
    """Tests for :class:`~exa.cms.isotope.Element`."""
    def setUp(self):
        """Test is performed on hydrogen."""
        iso = Isotope.to_frame()
        self.isotopes = iso[iso['name'] == "hydrogen"]

    def test_from_isotopes(self):
        """Test :func:`~exa.cms.isotope.Element.from_isotopes`."""
        try:
            element = Element.from_isotopes(self.isotopes)
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(element, Element)
        self.assertTrue(np.isclose(element.mass, 1.0079105192))

    def test_from_symbol_name(self):
        """
        Test :func:`~exa.cms.isotope.Element.from_symbol` and
        :func:`~exa.cms.isotope.Element.from_name`.
        """
        try:
            h0 = Element.from_symbol("h")
            h1 = Element.from_name("hydrogen")
            h2 = Element.from_name("HYDROGEN")
        except Exception as e:
            self.fail(str(e))
        self.assertTrue(np.isclose(h0.mass, h1.mass))
        self.assertTrue(np.isclose(h0.mass, h2.mass))

    def test_all_elements(self):
        """
        Test generation of all elements (:func:`~exa.cms.isotopes.elements`).
        """
        try:
            elementz = elements()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(elementz, pd.Series)
        self.assertIsInstance(elementz['hydrogen'], Element)
        self.assertTrue(np.isclose(elementz['hydrogen'].mass, 1.0079105192))

    def test_repr(self):
        """Test :class:`~exa.cms.isotope.Element` repr."""
        self.assertIsInstance(repr(Element.from_symbol('H')), string_types)


class TestMappers(UnitTester):
    """Test isotope/element mappers provided in :mod:`~exa.cms.isotope`."""
    def test_symbol_to_z(self):
        """
        Tests for :func:`~exa.cms.isotope.symbol_to_znum` and
        :func:`~exa.cms.isotope.znum_to_symbol`.
        """
        try:
            mapper0 = symbol_to_znum()
        except Exception as e:
            self.fail(str(e))
        try:
            mapper1 = znum_to_symbol()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(mapper0, pd.Series)
        self.assertIsInstance(mapper1, pd.Series)
        self.assertEqual(len(mapper0), len(mapper1))

    def test_symbol_to_radii(self):
        """Test :func:`~exa.cms.isotope.symbol_to_radius`."""
        try:
            mapper = symbol_to_radius()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(mapper, pd.Series)
        self.assertTrue(np.isclose(mapper['H'], 0.60471232))

    def test_symbol_to_mass(self):
        """Test :func:`~exa.cms.isotope.symbol_to_mass`."""
        try:
            mapper = symbol_to_mass()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(mapper, pd.Series)
        self.assertTrue(np.isclose(mapper['H'], 1.0079105192))

    def test_symbol_to_color(self):
        """Test :func:`~exa.cms.isotope.symbol_to_color`."""
        try:
            mapper = symbol_to_color()
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(mapper, pd.Series)
        self.assertTrue(mapper['H'], 10197915)
