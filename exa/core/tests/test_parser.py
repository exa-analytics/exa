# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Sections and Parsers
#############################################
Test the :class:`~exa.core.parser.Parser` object.
"""
#from unittest import TestCase
#from exa.core.editor import Editor
#from exa.core.parser import Sections, Parser
#from exa.typed import TypedProperty
#
#
#example = """header text
#====
#starting text
#----
#section 01 text
#----
#after section 01
#----
#section 02 text
#----
#after section 02
#----
#1.0 1.0 1.0
#----
#ending text
#====
#footer text
#"""
#
#
#class TestParser(TestCase):
#    """
#    """
#    def test_
#
#
#
#
#
#
##sections0 = u"""Sections have some text followed by a delimiter
##==================================
##that eventually repeats
##==================================
##"""
##
##
##sections1 = u"""Sections have some text followed by a delimiter
##==================================
##that eventually repeats
##==================================
##or may have final text.
##"""
##
##
##sections2 = u"""==============================
##Sections have some text preceded by a delimiter
##==================================
##that eventually repeats.
##==================================
##"""
##
##
##sections3 = u"""==============================
##Sections have some text preceded by a delimiter
##==================================
##that eventually repeats
##==================================
##or may have final text.
##"""
##
##
##class MockParser(Parser):
##    """Mock example of :class:`~exa.core.editor.Parser`."""
##    wordcount = TypedProperty(int, "Count of the number of words")
##    wordlist = TypedProperty(list, "List of words")
##
##    def _parse(self, fail=False):
##        """Parse a word section."""
##        self.wordlist = [word for line in self._lines for word in line.split()]
##        if not fail:
##            self.wordcount = len(self.wordlist)
##
##
##class MockSections(Sections):
##    """Mock example of :class:`~exa.core.editor.Sections`."""
##    _marker = "===="
##
##    def _parse(self, fail=False):
##        """This is depends on the file structure."""
##        delims = self.find(self._marker, text=False)[self._marker]
##        starts = [delim + 1 for delim in delims]
##        starts.insert(0, 0)
##        ends = delims
##        ends.append(len(self))
##        names = [MockParser]*len(starts)
##        names[-1] = "none"
##        if not fail:
##            self._sections_helper(names, starts, ends)
##
##
##class TestParser(TestCase):
##    """
##    Tests for :class:`~exa.core.parser.Sections` and
##    :class:`~exa.core.parser.Parser`.
##    """
##    def test_basic_parsing(self):
##        """Test live modification of class objects on parsing."""
##        sec = MockSections(sections0)
##        self.assertFalse(hasattr(sec, "section0"))
##        self.assertFalse(hasattr(sec, "parse_section0"))
##        sec.parse()
##        for i in sec.sections.index:
##            attrname = sec.sections.loc[i, "attribute"]
##            self.assertTrue(hasattr(sec, attrname))
##        sec.section1.parse()
##        self.assertTrue(hasattr(sec.section0, "wordlist"))
##        self.assertTrue(hasattr(sec.section0, "wordcount"))
##        self.assertTrue(sec.section1.wordcount > 0)
##
##    def test_recursive_parsing(self):
##        """Test recursive parsing."""
##        sec = MockSections(sections1)
##        self.assertFalse(hasattr(sec, "section0"))
##        self.assertFalse(hasattr(sec, "parse_section0"))
##        sec.parse(recursive=True)
##        for i in sec.sections.index:
##            attrname = sec.sections.loc[i, "attribute"]
##            self.assertTrue(hasattr(sec, attrname))
##        sec.section1.parse()
##        self.assertTrue(hasattr(sec.section0, "wordlist"))
##        self.assertTrue(hasattr(sec.section0, "wordcount"))
##        self.assertTrue(sec.section1.wordcount > 0)
##
##    def test_verbose_parsing(self):
##        """Test both recursive and verbose options."""
##        sec = MockSections(sections2)
##        self.assertFalse(hasattr(sec, "section1"))
##        self.assertFalse(hasattr(sec, "parse_section1"))
##        sec.parse(recursive=True)
##        for i in sec.sections.index:
##            attrname = sec.sections.loc[i, "attribute"]
##            self.assertTrue(hasattr(sec, attrname))
##        sec.section1.parse(verbose=True, recursive=True)
##        self.assertTrue(hasattr(sec.section0, "wordlist"))
##        self.assertTrue(hasattr(sec.section0, "wordcount"))
##        self.assertTrue(sec.section1.wordcount > 0)
##
##    def test_fallback_parsing(self):
##        """Test that missing parsers fallback to Editors."""
##        # Test section without a parser class (see above)
##        sec3 = MockSections(sections3)
##        with self.assertRaises(ValueError):
##            sec3.parse(fail=True)    # Also tests keyword args pass through
##        sec3.parse()
##        self.assertTrue(hasattr(sec3, "section2"))    # Default parsing of section to a generic Editor
##        self.assertFalse(hasattr(sec3.section3, "parse"))
##        self.assertFalse(isinstance(sec3.section3, (Parser, Sections)))
##        self.assertIsInstance(sec3.section3, Editor)
##
##    def test_get_section(self):
##        """Test :func:`~exa.core.parsing.Sections.get_section`."""
##        sections = MockSections(sections0)
##        sections.parse(recursive=True)
##        sec = sections.get_section(0)
##        self.assertTrue(sec is sections.section0)
##        sec = sections.get_section("none")
##        self.assertTrue(sec is sections.section2)
##        with self.assertRaises(ValueError):
##            sections.get_section("MockParser")
##        with self.assertRaises(TypeError):
##            sections.get_section(1.5)
##        with self.assertRaises(KeyError):
##            sections.get_section(5)
