# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.editor`
#############################################
Test the functionality of the :class:`~exa.core.editor.Editor` class and
related functions.
"""
import os
import bz2
import gzip
import six
import shutil
import numpy as np
from io import StringIO
from uuid import uuid4
from exa._config import config
from exa.tester import UnitTester
from exa.core.editor import Editor, concat
if not hasattr(bz2, "open"):
    bz2.open = bz2.BZ2File


editor_string = u"""This string is used as the test for the editor class.

That was a blank line
It contains templates: {template}
and constants: {{constant}}

That was a blank line"""


class TestEditor(UnitTester):
    """
    The tester reads in a contrived example in the root "tests" directory and
    proceeds to test the various functions provided by
    :class:`~exa.core.editor.Editor`.
    """
    def setUp(self):
        """
        A :class:`~exa.core.editor.Editor` can be create in three ways,
        from a file, from a stream, and from a string.
        """
        self.path = os.path.join(config['paths']['tmp'], uuid4().hex)
        with open(self.path, 'wb') as f:
            f.write(editor_string.encode())
        with open(self.path, "rb") as f_in:
            with gzip.open(self.path + ".gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        with open(self.path, "rb") as f_in:
            with bz2.open(self.path + ".bz2", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        with open(self.path + '.iso-8859-1', 'wb') as f:
            f.write(editor_string.encode('iso-8859-1'))
        self.from_file = Editor(self.path)
        self.from_file_enc = Editor(self.path, encoding='iso-8859-1')
        self.from_gzip = Editor(self.path + ".gz")
        self.from_bz2 = Editor(self.path + ".bz2")
        self.from_stream = Editor(StringIO(editor_string))
        self.from_string = Editor(editor_string)

    def tearDown(self):
        """Remove the temporary files generated by the test."""
        os.remove(self.path)
        os.remove(self.path + ".gz")
        os.remove(self.path + ".bz2")
        os.remove(self.path + ".iso-8859-1")

    def test_editor_input_methods(self):
        """
        Test to make sure all the support input (**read_\***) were read in
        correctly. This function actually tests
        :func:`~exa.core.editor.Editor.__eq__`.
        """
        self.assertEqual(self.from_file, self.from_file_enc)
        self.assertEqual(self.from_file, self.from_gzip)
        self.assertEqual(self.from_file, self.from_bz2)
        self.assertEqual(self.from_file, self.from_stream)
        self.assertEqual(self.from_file, self.from_string)

    def test_tmpl_cnst(self):
        """
        Test :func:`~exa.core.editor.Editor.templates`,
        :func:`~exa.core.editor.Editor.constants`,
        and, by proxy, :func:`~exa.core.editor.Editor.regex`.
        """
        self.assertEqual(self.from_file.templates, ['template'])
        self.assertEqual(self.from_file.constants, ['constant'])
        cnst = u"{{[\w\d]*}}"
        self.assertEqual(len(self.from_file.regex(cnst)[cnst]), 1)
        cnst = u"{[\w\d]*}"
        self.assertEqual(len(self.from_file.regex(cnst)[cnst]), 2)
        cnst = u"{[\w\d]*}"
        self.assertEqual(len(self.from_file.regex(cnst, which='keys')[cnst]), 2)

    def test_head_tail(self):
        """
        Test :func:`~exa.core.editor.Editor.head` and
        :func:`~exa.core.editor.Editor.tail`.
        """
        self.assertEqual(self.from_file.head(1), self.from_file._lines[0])
        self.assertEqual(self.from_file.tail(1), self.from_file._lines[-1])

    def test_insert(self):
        """
        Test :func:`~exa.core.editor.Editor.append`,
        Test :func:`~exa.core.editor.Editor.prepend`, and
        :func:`~exa.core.editor.Editor.insert`.
        """
        test = "new\nlines"
        self.from_file.append(test)
        self.assertEqual(str(self.from_file[-1]), "lines")
        self.from_file.prepend(test)
        self.assertEqual(str(self.from_file[1]), "lines")
        del self.from_file[0]
        del self.from_file[0]
        del self.from_file[-1]
        del self.from_file[-1]
        self.from_file.insert(-1, test)
        self.assertEqual(str(self.from_file[-2]), "lines")
        del self.from_file[-2]
        del self.from_file[-2]
        test = test.splitlines()
        self.from_file.append(test)
        self.assertEqual(str(self.from_file[-1]), "lines")
        self.from_file.prepend(test)
        self.assertEqual(str(self.from_file[1]), "lines")
        del self.from_file[0]
        del self.from_file[0]
        del self.from_file[-1]
        del self.from_file[-1]
        self.from_file.insert(-1, test)
        self.assertEqual(str(self.from_file[-2]), "lines")
        del self.from_file[-2]
        del self.from_file[-2]
        with self.assertRaises(TypeError):
            self.from_file.insert(2, 10)
        with self.assertRaises(TypeError):
            self.from_file.append(10)
        with self.assertRaises(TypeError):
            self.from_file.prepend(10)

    def test_delete(self):
        """Test :func:`~exa.core.editor.Editor.__delitem__` specifically."""
        lines = np.unique(np.random.randint(0, len(self.from_gzip), size=(len(self.from_gzip), )))
        n0 = len(lines)
        n1 = len(self.from_gzip) - n0
        self.from_gzip.delete_lines(lines)
        self.assertEqual(len(self.from_gzip), n1)

    def test_replace(self):
        """Test :func:`~exa.core.editor.Editor.replace`."""
        rp0 = "This string is used as the test for the editor class."
        rp1 = "replacement"
        self.from_file.replace(rp0, rp1)
        self.assertEqual(str(self.from_file[0]), rp1)
        self.from_file.replace(rp1, rp0)

    def test_find(self):
        """Test :func:`~exa.core.editor.Editor.find`."""
        rp = "That was a blank line"
        self.assertEqual(len(self.from_file.find(rp)[rp]), 2)
        self.assertEqual(len(self.from_file.find(rp, which="keys")[rp]), 2)
        self.assertEqual(len(self.from_file.find(rp, which="values")[rp]), 2)

    def test_find_next(self):
        """Test :func:`~exa.core.editor.Editor.find_next`."""
        rp = "That was a blank line"
        self.assertEqual(self.from_file.find_next(rp, "keys", True), 6)  # Cursor 0 -> 6
        self.assertEqual(self.from_file.find_next(rp, "keys"), 2)        # 6 -> 2
        self.assertEqual(self.from_file.find_next(rp, "keys"), 6)        # 2 -> 6
        self.assertEqual(self.from_file.find_next(rp, "values"), rp)     # 2 -> 6
        self.assertEqual(self.from_file.find_next(rp), (6, rp))

    def test_concat(self):
        """Test :func:`~exa.core.editor.concat`."""
        ed = concat(self.from_file, self.from_file)
        self.assertEqual(len(ed), 2*len(self.from_file))

    def test_remove_blank_lines(self):
        """Test :func:`~exa.core.editor.Editor.remove_blank_lines`."""
        self.from_gzip.remove_blank_lines()
        self.assertEqual(len(self.from_gzip), len(self.from_file) - 2)

    def test_copy(self):
        """
        Test :func:`~exa.core.editor.Editor.copy` and ensure that slicing the
        editor returns a instance of an Editor.
        """
        cp = self.from_file.copy()
        self.assertEqual(self.from_file, cp)
        self.assertFalse(cp is self.from_file)
        self.assertIsInstance(self.from_file[0:2], Editor)

    def test_format(self):
        """
        Test :func:`~exa.core.editor.Editor.format` and by proxy test,
        :func:`~exa.core.editor.Editor.__contains__` and
        :func:`~exa.core.editor.Editor.__eq__` (false).
        """
        fmt = self.from_file.format(template="formatted")
        self.assertTrue("formatted" in fmt)
        self.from_gzip.format(template='formatted', inplace=True)
        self.assertTrue("formatted" in fmt)
        self.assertFalse(self.from_file == self.from_gzip)
        path = self.path + ".tmp"
        self.from_bz2.write(path)
        self.assertTrue(os.path.exists(path))
        os.remove(path)
        self.from_bz2.write(path, template="formatted")
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_read_missing_file(self):
        """Test reading a missing file."""
        path = os.path.abspath(__file__) + ".garbage"
        with self.assertRaises((OSError, IOError)):
            Editor(path)

    def test_repr(self):
        """Test :func:`~exa.core.editor.Editor.__repr__`."""
        self.assertIsInstance(self.from_file.__repr__(), six.string_types)
        self.from_gzip.nprint = 2
        self.assertIsInstance(self.from_gzip.__repr__(), six.string_types)
