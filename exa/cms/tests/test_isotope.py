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
from exa.tester import UnitTester
from exa.cms.isotope import (Isotope, Element, elements, symbol_to_znum,
                             znum_to_symbol)


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
        with self.assertRaises(KeyError):
            Isotope[-1]

    def test_compute_element(self):
        """
        Test :func:`~exa.cms.isotope.Isotope.element` and
        :func:`~exa.cms.isotope.Meta.compute_element`.
        """
        try:
            h = Isotope.element("H")
        except Exception as e:
            self.fail(str(e))
        self.assertTrue(np.isclose(h.mass, 1.0079105192))


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
        self.assertEqual(len(mapper0), len(mapper1) + 2)    # account for D & T

    def test_symbol_to_radii(self):
        """
        Tests for :func:`~exa.cms.isotope.symbol_to_radius` and
        :func:`~exa.cms.isotope.radius_to_symbol`.
        """
        pass
