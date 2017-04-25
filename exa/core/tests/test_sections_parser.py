# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Sections and Parsers`
#############################################
Tests for the related modules, :mod:`~exa.core.sections` and
:mod:`~exa.core.parsers`.
"""
import six
import pandas as pd
from unittest import TestCase
from exa.core.sections import Sections, SectionsMeta
from exa.core.parser import Parser


sections0 = u"""Sections have some text followed by a delimiter
==================================
that eventually repeats
==================================
"""


sections1 = u"""Sections have some text followed by a delimiter
==================================
that eventually repeats
==================================
or may have final text.
"""


sections2 = u"""==============================
Sections have some text preceded by a delimiter
==================================
that eventually repeats.
==================================
"""


sections3 = u"""==============================
Sections have some text preceded by a delimiter
==================================
that eventually repeats
==================================
or may have final text.
"""


class MockSections(Sections):
    """Mock example of :class:`~exa.core.editor.Sections`."""
    name = "example_sections"
    description = "Parses text sections delimited by ===="
    _key_marker = "===="
    _key_def_sec_name = 'default'

    def _parse(self):
        """This is depends on the file structure."""
        delims = self.find(self._key_marker, which='lineno')[self._key_marker]
        starts = [delim + 1 for delim in delims]
        starts.insert(0, 0)
        ends = delims
        ends.append(len(self))
        names = [self._key_def_sec_name]*len(starts)
        dct = {"parser": names, "start": starts, "end": ends}
        self._sections_helper(dct)


class MockSectionMeta(SectionsMeta):
    """Metaclass that defines data objects for the section parser."""
    wordcount = int
    wordlist = list
    _descriptions = {'wordcount': "Count of number of words",
                     'wordlist': "List of words"}


class MockParser(six.with_metaclass(MockSectionMeta, Parser)):
    """Mock example of :class:`~exa.core.editor.Parser`."""
    name = "default"
    description = "Parser for word regions."

    def _parse(self):
        """Parse a word section."""
        self.wordlist = [word for line in self._lines for word in line.split()]
        self.wordcount = len(self.wordlist)


class MockBaseSections(Sections):
    """Raises TypeError."""
    pass


class MockBaseParser(Parser):
    """Raises TypeError."""
    pass


MockSections.add_section_parsers(MockParser)


class TestSections(TestCase):
    """
    Tests for :class:`~exa.core.editor.Sections`. and
    :class:`~exa.core.editor.Parser.`
    """
    def test_base_sections(self):
        """Tests raising TypeError."""
        with self.assertRaises(TypeError):
            MockBaseSections()
        with self.assertRaises(TypeError):
            MockBaseParser()

    def test_describe_pre_parse(self):
        """Test descriptors prior to parsing."""
        sec0 = MockSections(sections0)
        sec1 = MockSections(sections1)
        sec2 = MockSections(sections2)
        sec3 = MockSections(sections3)
        secs = [sec0, sec1, sec2, sec3]
        for sec in secs:
            df = sec.describe()
            self.assertIsInstance(df, pd.Series)
            self.assertEqual(len(df), 4)
            df = sec.describe_parsers()
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(len(df), 1)

    def test_parsing(self):
        """Test live modification of class objects on parsing."""
        sec0 = MockSections(sections0)
        sec1 = MockSections(sections1)
        sec2 = MockSections(sections2)
        sec3 = MockSections(sections3)
        secs = [sec0, sec1, sec2, sec3]
        for sec in secs:
            self.assertFalse(hasattr(sec, "section0"))
            self.assertFalse(hasattr(sec, "parse_section0"))
            sec.parse()
            for i in sec.sections.index:
                attrname = sec.sections.loc[i, "attr"]
                self.assertTrue(hasattr(sec, attrname))
            sec.section1.parse()
            self.assertTrue(hasattr(sec.section0, "wordlist"))
            self.assertTrue(hasattr(sec.section0, "wordcount"))
            self.assertTrue(sec.section1.wordcount > 0)
