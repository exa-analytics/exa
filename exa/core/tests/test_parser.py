# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.parser`
#############################################
Parsing is tested on static data provided in the included data directory.
"""
#import six, re
#import pandas as pd
#from unittest import TestCase
#from exa import Typed
#from exa.static import resource
#from exa.core.parser import Parser, Sections
#
#
## Simple test parsers
#class SCF(Parser):
#    """
#    Test find and regex section searches.
#
#    Because no **_parse** method is implemented, this parser doesn't
#    actually transform and text to data objects.
#    """
#    _start = "Self-consistent Calculation"
#    _end = re.compile("^\s*End of self-consistent calculation$", re.MULTILINE)
#
#
#class XYZ(Parser):
#    """Test regex and custom section searches."""
#    _start = re.compile("^ATOMIC_POSITIONS", re.MULTILINE)
#    _endregex = re.compile("^\s*$")
#    atom = Typed(pd.DataFrame, doc="XYZ-like table of nuclear coordinates")
#
#    def _parse_end(self, starts):
#        # Special parser for ends
#        r = self._endregex
#        return [self.regex_next(r, cursor=match[0]) for match in starts]
#
#    def parse_atom(self):
#        self.atom = pd.read_csv(self[1:-2].to_stream(),
#                                names=("symbol", "x", "y", "z"),
#                                delim_whitespace=True)
#
#
#class Output(Parser):
#    """Test generic parser wrapper."""
#    pass
#
#
#Output.add_parsers(SCF, XYZ)
#
#
## Testing begins here
#class TestSections(TestCase):
#    """Test the sections dataframe works correctly."""
#    def test_create(self):
#        sec = Sections.from_lists([0], [0], [None])
#        self.assertIsInstance(sec['startline'].tolist()[0], six.integer_types)
#        self.assertEqual(len(sec), 1)
#
#    def test_empty_get(self):
#        sec = Sections.from_lists([0], [0], [None])
#        with self.assertRaises(AttributeError):
#            sec.get_section(0)
#
#
#class TestParser(TestCase):
#    """Check basic parsing functionality on a test file."""
#    def setUp(self):
#        self.ed = Output(resource("parser.bz2"))
#
#    def test_basic(self):
#        self.assertEqual(len(self.ed), 2002)
#
#    def test_sections(self):
#        sec = self.ed.sections
#        self.assertEqual(len(sec), 10)
#
#    def test_get_section(self):
#        """Test section getting and alternate getitem lookup."""
#        ed = self.ed.get_section(-1)
#        self.assertIsInstance(ed, XYZ)
#        self.assertEqual(len(ed.atom), 3)
#
#    def test_info(self):
#        df = self.ed.info()
#        self.assertEqual(len(df), 1)
#        self.assertIn("atom", df['name'].values)
