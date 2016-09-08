# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.editor`
#################################
Test the features and functionality of the :class:`~exa.editor.Editor` object.
"""
#from exa._config import config
#from exa.test import UnitTester
#from exa.editor import Editor
#from exa.utility import mkp
#
#
#class TestEditor(UnitTester):
#    """
#    Test for the :class:`~exa.editor.Editor` are performed on the editor's
#    source code itself.
#    """
#    def setUp(self):
#        """
#        Generate the file path to the exa.editor module (which will be used as
#        the test for the :class:`~exa.editor.Editor` class that it provides).
#        """
#        self.path = mkp(config['dynamic']['pkgdir'], 'editor.py')
#        with open(self.path) as f:
#            self.lines = f.readlines()
#        self.fl = Editor.from_file(self.path)
#
#    def test_loaders(self):
#        """
#        The editor provides there different methods for instantiation; from a
#        file on disk, from a file stream, or from a string.
#        """
#        fl = Editor.from_file(self.path)
#        with open(self.path) as f:
#            tm = Editor.from_stream(f)
#            f.seek(0)
#            tr = Editor.from_string(f.read())
#        self.assertTrue(len(self.lines) == len(fl) == len(tm) == len(tr))
#        self.assertTrue(all(fl[i] == tm[i] == tr[i] for i in range(len(self.lines))))
#
#    def test_find_regex(self):
#        """
#        Test :func:`~exa.editor.Editor.find`, :func:`~exa.editor.Editor.regex`,
#        and :func:`~exa.editor.Editor.find_next`. Also checks cursor behavior.
#        """
#        od = self.fl.find('Args:')
#        self.assertIsInstance(od, list)
#        self.assertIsInstance(od[0], tuple)
#        self.assertTrue(len(od) == 16)
#        self.assertTrue(self.fl.cursor == 0)
#        n0, line0 = self.fl.find_next('Args:')
#        self.assertIsInstance(n0, int)
#        self.assertIsInstance(line0, str)
#        self.assertIn(n0, od[0])
#        self.assertTrue(self.fl.cursor > 0)
#        n1, line1 = self.fl.find_next('Args:')
#        self.assertTrue(n1 > n0)
#        self.assertIsInstance(line1, str)
#        self.assertIn(n1, od[1])
#        od1 = self.fl.regex('Args:')
#        self.assertTrue(od == od1)    # True in this case; depends on regex used
#
#    def test_insert_format_plus(self):
#        """
#        Test :func:`~exa.editor.Editor.insert` and :func:`~exa.editor.Editor.format`
#        functions. Also checks item deletion, :func:`~exa.editor.Editor.delete_lines`,
#        and __repr__, __iter__, __len__, __setitem__, __getitem__, and __str__.
#        Finally checks the variables property.
#        """
#        n = len(self.fl)
#        lines = {0: '{INSERTED}'}
#        self.fl.insert(lines)
#        self.assertTrue(len(self.fl) == n + 1)
#        self.assertTrue(self.fl[0] == lines[0])
#        self.fl.delete_lines(range(5, len(self.fl)))
#        self.assertTrue(len(self.fl) == 5)
#        self.assertTrue(len(self.fl.variables) == 1)
#        formatted = self.fl.format(INSERTED='replaced').splitlines()
#        self.assertTrue(formatted[0] == 'replaced')
#        del self.fl[0]
#        self.assertTrue(len(self.fl) == 4)
#
