# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.editor`
#################################
"""
import os, six
from unittest import TestCase
from exa import Editor


class TestEditor(TestCase):
    def setUp(self):
        """
        Generate the file path to the exa.core.editor module (which will be used as
        the test for the :class:`~exa.core.editor.Editor` class that it provides).
        """
        self.path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../editor.py"))
        with open(self.path) as f:
            self.lines = f.readlines()
        self.fl = Editor.from_file(self.path)

    def test_loaders(self):
        """
        The editor provides there different methods for instantiation; from a
        file on disk, from a file stream, or from a string.
        """
        fl = Editor.from_file(self.path)
        with open(self.path) as f:
            tm = Editor.from_stream(f)
            f.seek(0)
            tr = Editor.from_string(f.read())
        self.assertTrue(len(self.lines) == len(fl) == len(tm) == len(tr))
        self.assertTrue(all(fl[i] == tm[i] == tr[i] for i in range(len(self.lines))))

    def test_find_regex(self):
        od = self.fl.find('Args:')
        self.assertIsInstance(od, list)
        self.assertIsInstance(od[0], tuple)
        self.assertTrue(len(od) == 16)
        self.assertTrue(self.fl.cursor == 0)
        n0, line0 = self.fl.find_next('Args:')
        self.assertIsInstance(n0, int)
        self.assertIsInstance(line0, six.string_types)
        self.assertIn(n0, od[0])
        self.assertTrue(self.fl.cursor > 0)
        n1, line1 = self.fl.find_next('Args:')
        self.assertTrue(n1 > n0)
        self.assertIsInstance(line1, six.string_types)
        self.assertIn(n1, od[1])
        od1 = self.fl.regex('Args:')
        self.assertTrue(od == od1)    # True in this case; depends on regex used

    def test_insert_format_plus(self):
        n = len(self.fl)
        lines = {0: '{INSERTED}'}
        self.fl.insert(lines)
        self.assertTrue(len(self.fl) == n + 1)
        self.assertTrue(self.fl[0] == lines[0])
        self.fl.delete_lines(range(5, len(self.fl)))
        self.assertTrue(len(self.fl) == 5)
        self.assertTrue(len(self.fl.variables) == 1)
        formatted = self.fl.format(INSERTED='replaced').splitlines()
        self.assertTrue(formatted[0] == 'replaced')
        del self.fl[0]
        self.assertTrue(len(self.fl) == 4)
