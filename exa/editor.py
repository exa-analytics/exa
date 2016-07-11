# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Editor
####################################
Text-editor-like functionality for programatically manipulating raw text input
and output data and converting this data into container objects. This class
does not behave like a fully fledged text editor but does have some basic find,
replace, insert, etc. functionality.
'''
import os
import re
import sys
from io import StringIO, TextIOWrapper
from collections import OrderedDict


class Editor:
    '''
    An editor is a representation of a text file on disk that can be
    programmatically manipulated.

    Text lines are stored in memory; no files remain open. This class does not
    strive to be a fully fledged text editor rather a base class for converting
    input and output data from text on disk to some type of (exa framework)
    container object (and vice versa).

    >>> template = "Hello World!\\nHello {user}"
    >>> editor = Editor(template)
    >>> editor[0]
    'Hello World!'
    >>> len(editor)
    2
    >>> del editor[0]
    >>> len(editor)
    1
    >>> editor.write(fullpath=None, user='Alice')
    Hello Alice

    Tip:
        Editor line numbers use a 0 base index. To increase the number of lines
        displayed by the repr, increase the value of the **nprint** attribute.

    Warning:
        For large text with repeating strings be sure to use the **as_interned**
        argument.

    Attributes:
        name (str): Data/file/misc name
        description (str): Data/file/misc description
        meta (dict): Additional metadata as key, value pairs
        nrpint (int): Number of lines to display when printing
        cursor (int): Line number position of the cusor (see :func:`~exa.editor.Editor.find_next_any` and :func:`~exa.editor.Editor.find_next_string`)
    '''
    _getter_prefix = 'parse'
    _fmt = '{0}: {1}\n'.format   # Format for printing lines (see __repr__)

    def write(self, path=None, *args, **kwargs):
        '''
        Perform formatting and write the formatted string to a file or stdout.

        Optional arguments can be used to format the editor's contents. If no
        file path is given, prints to standard output.

        Args:
            path (str): Full file path (default None, prints to stdout)
            *args: Positional arguments to format the editor with
            **kwargs: Keyword arguments to format the editor with
        '''
        if path is None:
            print(self.format(*args, **kwargs))
        else:
            with open(path, 'w') as f:
                f.write(self.format(*args, **kwargs))

    def format(self, *args, inplace=False, **kwargs):
        '''
        Format the string representation of the editor.

        Args:
            inplace (bool): If True, overwrite editor's contents with formatted contents
        '''
        if not inplace:
            return str(self).format(*args, **kwargs)
        self._lines = str(self).format(*args, **kwargs).splitlines()

    def head(self, n=10):
        '''
        Display the top of the file.

        Args:
            n (int): Number of lines to display
        '''
        r = self.__repr__().split('\n')
        print('\n'.join(r[:n]), end=' ')

    def tail(self, n=10):
        '''
        Display the bottom of the file.

        Args:
            n (int): Number of lines to display
        '''
        r = self.__repr__().split('\n')
        print('\n'.join(r[-n:]), end=' ')

    def append(self, lines):
        '''
        Args:
            lines (list): List of line strings to append to the end of the editor
        '''
        if isinstance(lines, list):
            self._lines = self._lines + lines
        elif isinstance(lines, str):
            lines = lines.split('\n')
            self._lines = self._lines + lines
        else:
            raise TypeError('Unsupported type {0} for lines.'.format(type(lines)))

    def prepend(self, lines):
        '''
        Args:
            lines (list): List of line strings to insert at the beginning of the editor
        '''
        if isinstance(lines, list):
            self._lines = lines + self._lines
        elif isinstance(lines, str):
            lines = lines.split('\n')
            self._lines = lines + self._lines
        else:
            raise TypeError('Unsupported type {0} for lines.'.format(type(lines)))

    def insert(self, lines={}):
        '''
        Insert lines into the editor.

        Note:
            To insert before the first line, use :func:`~exa.editor.Editor.preappend`
            (or key 0); to insert after the last line use :func:`~exa.editor.Editor.append`.

        Args:
            lines (dict): Dictionary of lines of form (lineno, string) pairs
        '''
        for i, (key, line) in enumerate(lines.items()):
            n = key + i
            first_half = self._lines[:n]
            last_half = self._lines[n:]
            self._lines = first_half + [line] + last_half

    def remove_blank_lines(self):
        '''Remove all blank lines (blank lines are those with zero characters).'''
        to_remove = []
        for i, line in enumerate(self):
            ln = line.strip()
            if ln == '':
                to_remove.append(i)
        self.delete_lines(to_remove)

    def delete_lines(self, lines):
        '''
        Delete all lines with given line numbers.

        Args:
            lines (list): List of integers corresponding to line numbers to delete
        '''
        for k, i in enumerate(lines):
            del self[i-k]    # Accounts for the fact that len(self) decrease upon deletion

    def find(self, *strings):
        '''
        Search the entire editor for lines that match the string.

        Args:
            \*strings: Any number of strings to search for

        Returns:
            results (dict): Dictionary of string key, line values.
        '''
        results = {string: OrderedDict() for string in strings}
        for i, line in enumerate(self):
            for string in strings:
                if string in line:
                    results[string][i] = line
        return results

    def find_next(self, string):
        '''
        From the editor's current cursor position find the next instance of the
        given string.

        Args:
            string (str): String to search for from the current cursor position.
            reverse (bool): Search in reverse (default false)

        Returns:
            tup (tuple): Tuple of cursor position and line or None if not found

        Note:
            This function cycles the entire editor (i.e. cursor to length of
            editor to zero and back to cursor position).
        '''
        for start, stop in [(self.cursor, len(self)), (0, self.cursor)]:
            for i in range(start, stop):
                if string in self[i]:
                    tup = (i, self[i])
                    self.cursor = i + 1
                    return tup

    def regex(self, *patterns, line=False):
        '''
        Search the editor for lines matching the regular expression.

        Args:
            \*patterns: Regular expressions to search each line for
            line (bool): Return the whole line or the matched groups (groups default)

        Returns:
            results (dict): Dictionary of pattern keys, line values (or groups - default)
        '''
        results = {pattern: OrderedDict() for pattern in patterns}
        for i, line in enumerate(self):
            for pattern in patterns:
                grps = re.search(pattern, line)
                if grps:
                    grps = grps.groups()
                    if grps:
                        results[pattern][i] = grps
                    else:
                        results[pattern][i] = line
        return results

    def replace(self, pattern, replacement):
        '''
        Replace all instances of a pattern with a replacement.

        Args:
            pattern (str): Pattern to replace
            replacement (str): Text to insert
        '''
        for i in range(len(self)):
            line = self[i]
            while pattern in line:
                line = line.replace(pattern, replacement)
            self[i] = line

    @property
    def variables(self):
        '''
        Display a list of templatable variables present in the file.

        Templating is accomplished by creating a bracketed object in the same
        way that Python performs `string formatting`_. The editor is able to
        replace the placeholder value of the template. Integer templates are
        positional arguments.

        .. _string formatting: https://docs.python.org/3.6/library/string.html
        '''
        string = str(self)
        constants = [match[1:-1] for match in re.findall('{{[A-z0-9]}}', string)]
        variables = re.findall('{[A-z0-9]*}', string)
        return sorted(set(variables).difference(constants))

    @classmethod
    def from_file(cls, path, **kwargs):
        '''Create an editor instance from a file on disk.'''
        lines = lines_from_file(path)
        if 'meta' not in kwargs:
            kwargs['meta'] = {}
        kwargs['meta']['filepath'] = path
        return cls(lines, **kwargs)

    @classmethod
    def from_stream(cls, f, **kwargs):
        '''Create an editor instance from a file stream.'''
        lines = lines_from_stream(f)
        if 'meta' not in kwargs:
            kwargs['meta'] = {}
        kwargs['meta']['filepath'] = f.name if hasattr(f, 'name') else None
        return cls(lines, **kwargs)

    @classmethod
    def from_string(cls, string, **kwargs):
        '''Create an editor instance from a string template.'''
        return cls(lines_from_string(string), **kwargs)

    def __init__(self, path_stream_or_string, as_interned=False, nprint=30,
                 name=None, description=None, meta={}):
        if len(path_stream_or_string) < 256 and os.path.exists(path_stream_or_string):
            self._lines = lines_from_file(path_stream_or_string, as_interned)
        elif isinstance(path_stream_or_string, list):
            self._lines = path_stream_or_string
        elif isinstance(path_stream_or_string, (TextIOWrapper, StringIO)):
            self._lines = lines_from_stream(path_stream_or_string, as_interned)
        elif isinstance(path_stream_or_string, str):
            self._lines = lines_from_string(path_stream_or_string, as_interned)
        else:
            raise TypeError('Unknown type for arg data: {}'.format(type(data)))
        self.name = name
        self.description = description
        self.meta = meta
        self.nprint = 30
        self.cursor = 0

    def __delitem__(self, line):
        del self._lines[line]     # "line" is the line number minus one

    def __getitem__(self, key):
        if isinstance(key, str):
            return getattr(self, key)
        return self._lines[key]

    def __setitem__(self, line, value):
        self._lines[line] = value

    def __iter__(self):
        for line in self._lines:
            yield line

    def __len__(self):
        return len(self._lines)

    def __str__(self):
        return '\n'.join(self._lines)

    def __contains__(self, item):
        for obj in self:
            if item in obj:
                return True

    def __repr__(self):
        r = ''
        nn = len(self)
        n = len(str(nn))
        if nn > self.nprint * 2:
            for i in range(self.nprint):
                ln = str(i).rjust(n, ' ')
                r += self._fmt(ln, self._lines[i])
            r += '...\n'.rjust(n, ' ')
            for i in range(nn - self.nprint, nn):
                ln = str(i).rjust(n, ' ')
                r += self._fmt(ln, self._lines[i])
        else:
            for i, line in enumerate(self):
                ln = str(i).rjust(n, ' ')
                r += self._fmt(ln, line)
        return r


def lines_from_file(path, as_interned=False):
    '''
    Create a list of file lines from a given filepath.

    Args:
        path (str): File path
        as_interned (bool): List of "interned" strings (default False)

    Returns:
        strings (list): File line list
    '''
    lines = None
    with open(path) as f:
        if as_interned:
            lines = [sys.intern(line) for line in f.read().splitlines()]
        else:
            lines = f.read().splitlines()
    return lines


def lines_from_stream(f, as_interned=False):
    '''
    Create a list of file lines from a given file stream.

    Args:
        f (:class:`~io.TextIOWrapper): File stream
        as_interned (bool): List of "interned" strings (default False)

    Returns:
        strings (list): File line list
    '''
    if as_interned:
        return [sys.intern(line) for line in f.read().splitlines()]
    return f.read().splitlines()


def lines_from_string(string, as_interned=False):
    '''
    Create a list of file lines from a given string.

    Args:
        string (str): File string
        as_interned (bool): List of "interned" strings (default False)

    Returns:
        strings (list): File line list
    '''
    if as_interned:
        return [sys.intern(line) for line in string.splitlines()]
    return string.splitlines()
