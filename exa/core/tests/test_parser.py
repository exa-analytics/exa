# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.parser`
#############################################
Test the parsing engine on this file.
"""
from unittest import TestCase
from exa.core.parser import Parser, Sections
from exa.typed import Typed


class Docs(Parser):
    _s_cmd = 0
    _s_args = ("'''", '"""')
    text = Typed(str)

    def _parse(self):
        self.text = str(self.replace("'''", "").replace('"""', ""))


class CodeBlock(Parser):
    def _parse_sections(self):
        found = self.find(".. code-block::").all()
        start = []
        stop = []
        for m in found:
            indent = len(m.text) - len(m.text.lstrip(" "))
            for i, line in enumerate(self.lines[m.num+1:]):
                if len(line) - len(line.lstrip(" ")) == indent and line != "":
                    start.append(m.num)
                    stop.append(m.num + i + 1)
                    break
        self.sections = Sections(start, stop, [self.__class__]*len(start))


Docs.add_parsers(CodeBlock)


class TestParser(TestCase):
    pass
