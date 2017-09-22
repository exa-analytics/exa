# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.parser`
#############################################
Test the parsing engine on this file.
"""
from unittest import TestCase
from exa.core.parser import Parser


class SrcParser(Parser):
    """Top level parser for Python source code (testing)."""
    def _parse(self):
        """Only parses auxiliary text at the top of files."""
        pass


class DocString(Parser):
    """Docstring parser."""
    def _parse(self):
        """Parse docstrings."""
        df = list(self.find('"""', "'''").all().numpairs())


class PyFunc(Parser):
    """
    """
    pass


class PyClass(Parser):
    """
    """
    pass


class PyDocString(Parser):
    """
    """
    pass


class TestParser(TestCase):
    """Source code is a trivial example of a semi-structured file."""
    pass
