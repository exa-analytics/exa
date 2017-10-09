# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.parser`
#############################################
Parsing is tested on static data provided in the included data directory.
"""
import six, os, re
import pandas as pd
from unittest import TestCase
from exa.core.parser import Parser, Sections
from exa.typed import Typed
from exa.static import datadir


name = "parser.bz2"


# Simple test parsers
class SCF(Parser):
    """Test find and regex section searches."""
    _start = "Self-consistent Calculation"
    _end = re.compile("^\s*End of self-consistent calculation$", re.MULTILINE)


class XYZ(Parser):
    """Test regex and custom section searches."""
    _start = re.compile("^ATOMIC_POSITIONS", re.MULTILINE)
    _endregex = re.compile("^\s*$")

    def _parse_end(self, starts):
        # Special parser for ends
        r = self._endregex
        return [self.regex_next(r, cursor=match.num) for match in starts]

    def _parse(self):
        self.atom = pd.read_csv(self[1:].to_stream(),
                                names=("symbol", "x", "y", "z"),
                                delim_whitespace=True)


class Output(Parser):
    """Test generic parser wrapper."""
    pass


Output.add_parsers(SCF, XYZ)


# Testing begins here
class TestSections(TestCase):
    """Test the sections dataframe works correctly."""
    def test_create(self):
        sec = Sections.from_lists([0], [0], [None], None)
        self.assertIsInstance(sec['startline'].tolist()[0], six.integer_types)
        self.assertIsNone(sec._ed)
        self.assertEqual(len(sec), 1)

    def test_empty_get(self):
        sec = Sections.from_lists([0], [0], [None], None)
        with self.assertRaises(AttributeError):
            sec.get_section(0)


class TestParser(TestCase):
    """Check basic parsing functionality on a test file."""
    def setUp(self):
        self.ed = Output(os.path.join(datadir(), name))

    def test_basic(self):
        self.assertEqual(len(self.ed), 2002)

    def test_sections(self):
        sec = self.ed.sections
        self.assertEqual(len(sec), 10)

    def test_get_section(self):
        i = self.ed.sections[self.ed.sections['parser'] == XYZ].index[0]
        ed = self.ed.sections.get_section(i)
        self.assertIsInstance(ed, Parser)
        self.assertFalse(hasattr(ed, "atom"))
        ed.parse()
        self.assertTrue(hasattr(ed, "atom"))
        self.assertEqual(len(ed.atom), 3)
