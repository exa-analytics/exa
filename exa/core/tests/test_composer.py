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
    def test_dynamic(self):
        """Test that building a dynamic composer works."""
        comp = Composer("{}\n{labeled}\n{1: :lbl0}\n{1: :lbl1}\n{1:=:dct}",
                        1, labeled=5, lbl0=2, lbl1=3, dct={"four": 4})
        text = str(comp.compose())
        self.assertEqual(text, "1\n5\n3\n2\n4")

    def test_simple(self):
        """Test simple template."""
        comp = SimpleComposer(1, labeled="two")
        self.assertIsInstance(comp, Composer)
        self.assertEqual(str(comp.compose()), "1\ntwo")
