# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.composer`
#############################################
"""
#from unittest import TestCase
#from exa.core.composer import Composer
#
#
#template = r"""&control
#[control|4| = |'|]
#/
#[other|0|\||"|,] stuff and things [other1||||]
#{kw}
#{0}
#"""
#
#
#class Template(Composer):
#    """For testing purposes."""
#    _template = template
#
#
#class TestComposer(TestCase):
#    def test_basic(self):
#        """Test creating empty composers."""
#        with self.assertRaises(TypeError):
#            Composer()
#        simple = Composer(textobj="{0}")
#        self.assertIsInstance(simple, Composer)
#        self.assertListEqual(simple.lines, ["{0}"])
#
#    def test_basic_search(self):
#        simple = Composer(textobj="{0}")
#        found = simple.find("{")
#        self.assertEqual(len(found), 1)
#
#    def test_basic_fmt(self):
#        simple = Composer(textobj="{0}")
#        ret = simple.compose(1)
#        print(ret)
#        self.assertEqual(str(ret), "1")
#
#    def test_template_args(self):
#        tmp = Template("1", kw="2")
#        ret = tmp.compose()
#        self.assertEqual(str(ret[-1]), "1")
#        self.assertEqual(str(ret[-2]), "2")
