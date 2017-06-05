# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.composer`
#############################################
Test composer behavior.
"""
from unittest import TestCase
from exa.core.composer import Composer
from exa.typed import TypedProperty


class SimpleComposer(Composer):
    """
    Trivial composer used to test that original editor functionality has not
    been mangled.
    """
    _lines = "{}\n{labeled}"


class Cmpsr(Composer):
    """Type enforcing composer."""
    _lines = "{}\n{simple}\n{1: :line2}"
    line2 = TypedProperty(dict)
    line3 = TypedProperty(list)


class TestBasicComposer(TestCase):
    """
    Test dynamic composer creation and composers that utilize base editor
    features.
    """
    def test_get_compsers(self):
        """Test that ``_compose_`` methods are correctly identified."""
        composers = Composer("{}")._get_composers()
        self.assertIsInstance(composers, dict)
        self.assertEqual(len(composers), 4)
        self.assertIn("dict", composers)
        self.assertIn("tuple", composers)
        self.assertIn("list", composers)

    def test_dynamic(self):
        """Test that building a dynamic composer works."""
        comp = Composer("{0}\n{labeled}\n{1: :lbl0}\n\n{1:=:dct}",
                        1, labeled=5, lbl0=2, dct={"four": 4})
        self.assertListEqual(comp.templates, ["0", "labeled", "1: :lbl0", "1:=:dct"])
        text = str(comp.compose())
        self.assertEqual(text, "1\n5\n2\n\nfour=4")

    def test_simple(self):
        """Test simple template."""
        comp = SimpleComposer(1, labeled="two")
        self.assertIsInstance(comp, Composer)
        self.assertEqual(str(comp.compose()), "1\ntwo")
