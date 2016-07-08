# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Tests for :mod:`~exa.editor`
#################################
Test the features and functionality of the :class:`~exa.editor.Editor` object.
'''
from exa._config import config
from exa.test import UnitTester
from exa.editor import Editor
from exa.utility import mkp


class TestEditor(UnitTester):
    '''
    Test for the :class:`~exa.editor.Editor` are performed on the editor's
    source code itself.
    '''
    def setUp(self):
        '''
        Generate the file path to the exa.editor module (which will be used as
        the test for the :class:`~exa.editor.Editor` class that it provides).
        '''
        self.path = mkp(config['dynamic']['pkgdir'], 'editor.py')
        with open(self.path) as f:
            self.lines = f.readlines()

    def test_loaders(self):
        '''
        The editor provides there different methods for instantiation; from a
        file on disk, from a file stream, or from a string.
        '''
        file_ed = Editor.from_file(self.path)
        with open(self.path) as f:
            stream_ed = Editor.from_stream(f)
            f.seek(0)
            string_ed = Editor.from_string(f.read())
        self.assertTrue(len(self.lines) == len(file_ed) == len(stream_ed) == len(string_ed))
        i = np.random.randint(0, len(self.lines))
        self.assertTrue(stream_ed[i] == file_ed[i] == string_ed[i])
