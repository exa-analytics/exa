# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.composer`
#############################################
Test composer behavior.
"""
import six
from unittest import TestCase
from exa.core.composer import Composer, ComposerMeta


class SimpleComposer(Composer):
    """
    Trivial composer used to test that original editor functionality has not
    been mangled.
    """
    _template = "{}\n{labeled}"


class CmpsrMeta(ComposerMeta):
    """Data objects for more complex composer."""
    line2 = dict
    line3 = list


class Cmpsr(six.with_metaclass(CmpsrMeta, Composer)):
    """Type enforcing composer."""
    _template = "{}\n{simple}\n{1: :line2}"


class TestBasicComposer(TestCase):
    """
    Test dynamic composer creation and composers that utilize base editor
    features.
    """
    def test_get_compsers(self):
        """Test that ``_compose_`` methods are correctly identified."""
        composers = Composer("")._get_composers()
        self.assertIsInstance(composers, dict)
        self.assertEqual(len(composers), 5)
        self.assertIn("dict", composers)
        self.assertIn("str", composers)
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
