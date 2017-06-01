# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Editor
####################################
The :class:`~exa.core.editor.Editor` class is a way for programmatic manipulation
of text files (read in from disk). The purpose of this class is to facilitate
conversion of :class:`~exa.core.container.Container` objects to text (and vice
versa). This class also provides the base for text file parsing classes in
:mod:`~exa.core.parsing`.

.. code-block:: python

    editor = Editor(file.txt)       # Create an editor from a file
    editor = Editor(file.txt.gz)    # Automatically decompresses files
    editor = Editor(file.txt.bz2)
    for line in editor:             # Iterate over lines in the file
        pass
    if 'text' in editor:            # True if "text" appears on any line
        pass

Text lines are stored in memory; file handles are only open during reading and
writing. For large repetitive files, memoization can reduce the memory footprint
(see the **as_interned** kwarg).

Warning:
    The :class:`~exa.core.editor.Editor` is not a fully-featured text editor.

See Also:
    :mod:`~exa.core.parsing`
"""
import pandas as pd
from copy import copy, deepcopy
from collections import defaultdict
from itertools import chain
from io import StringIO, TextIOWrapper
import os, re, sys, bz2, gzip, six, json
from .base import Base
from exa.special import Typed
if not hasattr(bz2, "open"):
    bz2.open = bz2.BZ2File


class EditorMeta(Typed):
    """Typed attributes for editors."""
    name = str
    description = str
    meta = dict


class Editor(six.with_metaclass(EditorMeta, Base)):
    """
    In memory text file-like object used to facilitate data parsing and
    container to text conversion.

    Args:
        data: File path, text, stream, or archived text file
        as_intered (bool): Memory saving for large, repeating, files
        nprint (int): Number of lines shown by the 'repr'
        encoding (str): File encoding
        meta (dict): Metadata
        path_check (bool): Force file path check (default true)
        ignore_warning (bool): Ignore file path warning (default false)

    Attributes:
        cursor (int): Line number of cursor
        _fmt (str): Format string for display ('repr')
        _std_tmpl (str): Standard Python string template
        _exa_tmpl (str): Special string template
        _cnst (str): Regex for identifying constants
        _tmpl (str): Regex for identifying templates

    See Also:
        :class:`~exa.core.composer.Compser`s are useful for building text
        files programmatically. The :mod:`~exa.core.parser` module provides
        classes useful for programatic parsing of text files.
    """
    _getters = ("_get", "parse")
    _fmt = "{0}: {1}\n".format
    _std_tmpl = "{.+}"
    _exa_tmpl = "{.+:.*:.+}"
    _cnst = "{{.+}}"

    @property
    def templates(self):
        """
        Display a list of Python string templates present in this text.

        .. code-block:: text

            tmpl = "this is a {template}"
            tmpl.format(template="other text")    # prints "this is a other text"

        See Also:
            `String formatting`_.

        .. _String formatting: https://docs.python.org/3.6/library/string.html
        """
        matches = self.regex(self._std_tmpl, self._exa_tmpl, self._cnst, num=False)
        constants = [match for match in matches[self._cnst]]
        templates = matches[self._std_tmpl] + matches[self._exa_tmpl]
        return sorted(set(templates).difference(constants))

    @property
    def constants(self):
        """
        Display test of literal curly braces.

        .. code-block:: text

            cnst = "this is a {{constant}}"   # Cannot be "formatted"

        See Also:
            `String formatting`_.

        .. _String formatting: https://docs.python.org/3.6/library/string.html
        """
        return sorted(self.regex(self._cnst, num=False)[self._cnst])

    def regex(self, *patterns, **kwargs):
        """
        Match a line or lines by the specified regular expression(s).

        Returned values may be a list of (number, text) pairs or a list of line
        numbers or a list of text strings.

        .. code-block:: python

            ed = Editor(text)
            ed.regex("^=+$")            # Returns (line number, text) pairs where the line contains only '='
            ed.regex("^=+$", "find")    # Search for multiple regex simultaneously

        Args:
            patterns: Regular expressions
            num (bool): Return line number (default true)
            text (bool): Return line text (default true)
            flags: Python regex flags (default re.MULTILINE)

        Returns:
            results (dict): Dictionary with pattern keys and list of values

        Note:
            By default, regular expression search multiple lines (``re.MULTILINE``).

        See Also:
            https://en.wikipedia.org/wiki/Regular_expression
        """
        num = kwargs.pop("num", True)
        text = kwargs.pop("text", True)
        flags = kwargs.pop('flags', re.MULTILINE)
        results = defaultdict(list)
        self_str = str(self)
        for pattern in patterns:
            match = pattern
            if not type(pattern).__name__ == "SRE_Pattern":    # Compiled regular expression type check
                match = re.compile(pattern, flags)
            if num and text:
                for m in match.finditer(self_str):
                    results[match.pattern].append((self_str.count("\n", 0, m.start()) + 1, m.group()))
            elif num:
                for m in match.finditer(self_str):
                    results[match.pattern].append(self_str.count("\n", 0, m.start()) + 1)
            elif text:
                for m in match.finditer(self_str):
                    results[match.pattern].append(m.group())
            else:
                raise ValueError("At least one of ``num`` or ``text`` must be true.")
        return results

    def find(self, *patterns, **kwargs):
        """
        Search for patterns line by line.

        Args:
            strings (str): Any number of strings to search for
            num (bool): Return line number (default true)
            text (bool): Return line text (default true)

        Returns:
            results (dict): Dictionary with pattern keys and list of (lineno, line) values
        """
        num = kwargs.pop("num", True)
        text = kwargs.pop("text", True)
        results = defaultdict(list)
        for i, line in enumerate(self):
            for pattern in patterns:
                if pattern in line:
                    if num and text:
                        results[pattern].append((i, line))
                    elif num:
                        results[pattern].append(i)
                    elif text:
                        results[pattern].append(line)
                    else:
                        raise ValueError("At least one of ``num`` or ``text`` must be true.")
        return results

    def find_next(self, pattern, num=True, text=True, reverse=False):
        """
        From the current cursor position, find the next occurrence of the pattern.

        Args:
            pattern (str): String to search for from the cursor
            num (bool): Return line number (default true)
            text (bool): Return line text (default true)
            reverse (bool): Find next in reverse (default false)

        Returns:
            tup (tuple): Tuple of line number and line of next occurrence

        Note:
            Searching will cycle the file and continue if an occurrence is not
            found (forward or reverse direction determined by ``reverse``).
        """
        n = len(self)
        n1 = n - 1
        if reverse:
            self.cursor = 0 if self.cursor == 0 else self.cursor - 1
            positions = [(self.cursor - 1, 0, -1), (n1, self.cursor, -1)]
        else:
            self.cursor = 0 if self.cursor == n1 else self.cursor + 1
            positions = [(self.cursor, n, 1), (0, self.cursor, 1)]
        for start, stop, inc in positions:
            for i in range(start, stop, inc):
                if pattern in str(self[i]):
                    self.cursor = i
                    if num and text:
                        return (i, str(self[i]))
                    elif num:
                        return i
                    elif text:
                        return str(self[i])
                    else:
                        raise ValueError("At least one of ``num`` or ``text`` must be true.")

    def copy(self):
        """Return a copy of the current editor."""
        special = ("_lines", "as_interned", "nprint", "meta", "encoding")
        cls = self.__class__
        lines = self._lines[:]
        as_interned = copy(self.as_interned)
        nprint = copy(self.nprint)
        meta = deepcopy(self.meta)
        encoding = copy(self.encoding)
        cp = {k: copy(v) for k, v in self._vars(True).items() if k not in special}
        return cls(lines, as_interned, nprint, meta, encoding, **cp)

    def format(self, *args, **kwargs):
        """
        Populate the editors templates.

        Args:
            args: Args for formatting
            kwargs: Kwargs for formatting
            inplace (bool): If True, overwrite editor's contents (default False)

        Returns:
            formatted: Returns the formatted editor (if inplace is False)
        """
        inplace = kwargs.pop("inplace", False)
        if inplace:
            self._lines = str(self).format(*args, **kwargs).splitlines()
        else:
            cp = self.copy()
            cp._lines = str(cp).format(*args, **kwargs).splitlines()
            return cp

    def write(self, path, *args, **kwargs):
        """
        Write the editor contents to a file.

        Args:
            path (str): Full file path (default none, prints to stdout)
            args: Positional arguments for formatting
            kwargs: Keyword arguments for formatting
        """
        with open(path, "wb") as f:
            if len(args) > 0 or len(kwargs) > 0:
                f.write(six.b(str(self.format(*args, **kwargs))))
            else:
                f.write(six.b(str(self)))

    def head(self, n=10):
        """Display the top of the file."""
        return "\n".join(self._lines[:n])

    def tail(self, n=10):
        """Display the bottom of the file."""
        return "\n".join(self._lines[-n:])

    def append(self, lines):
        """
        Append lines to the editor.

        Args:
            lines (list, str): List of lines or text to append to the editor

        Note:
            Occurs in-place, like ``list.append``.
        """
        if isinstance(lines, list):
            self._lines += lines
        elif isinstance(lines, six.string_types):
            self._lines += lines.splitlines()
        else:
            raise TypeError("Unsupported type {} for lines.".format(type(lines)))

    def prepend(self, lines):
        """
        Prepend lines to the editor.

        Args:
            lines (list, str): List of lines or text to append to the editor

        Note:
            Occurs in-place, like ``list.insert(0, ...)``.
        """
        if isinstance(lines, list):
            self._lines = lines + self._lines
        elif isinstance(lines, six.string_types):
            self._lines = lines.splitlines() + self._lines
        else:
            raise TypeError("Unsupported type {} for lines.".format(type(lines)))

    def insert(self, lineno, lines):
        """
        Insert lines into the editor after ``lineno``.

        Args:
            num (int): Line number after which to insert lines
            text (list, str): List of lines or text to append to the editor

        Note:
            Occurs in-place, like ``list.insert(...)``.
        """
        if isinstance(lines, six.string_types):
            lines = lines.splitlines()
        elif not isinstance(lines, list):
            raise TypeError("Unsupported type {} for lines.".format(type(lines)))
        self._lines = self._lines[:lineno] + lines + self._lines[lineno:]

    def replace(self, pattern, replacement, inplace=False):
        """
        Replace all instances of a pattern with a replacement.

        Args:
            pattern (str): Pattern to replace
            replacement (str): Text to insert

        """
        lines = []
        for line in self:
            lines.append(line.replace(pattern, replacement))
        if inplace:
            self._lines = lines
        else:
            new = self.copy()
            new._lines = lines
            return new

    def remove_blank_lines(self):
        """Remove all blank lines (blank lines are those with zero characters)."""
        to_remove = []
        for i, line in enumerate(self):
            ln = line.strip()
            if ln == '':
                to_remove.append(i)
        self.delete_lines(to_remove)

    def delete_lines(self, lines):
        """
        Delete all lines with given line numbers.

        Args:
            lines (list): List of integers corresponding to line numbers to delete
        """
        for k, i in enumerate(sorted(lines)):
            del self[i-k]

    def iterlines(self, start=0, stop=None, step=None):
        """Line generator."""
        for line in self._lines[slice(start, stop, step)]:
            yield line

    def info(self):
        """
        Describe the current editor object.

        By default, the editor class displays the length of the text and the
        file name (if applicable).
        """
        return {'length': len(self),
                'file': self.meta['filepath'] if self.meta is not None and "filepath" in self.meta else "NA",
                'type': type(self)}

    def to_stream(self):
        """Send editor text to a file stream (StringIO) object."""
        return StringIO(six.u(str(self)))

    def to_file(self, path, *args, **kwargs):
        """Convenience name for :func:`~exa.core.editor.Editor.write`."""
        self.write(path, *args, **kwargs)

    def to_data(self, kind='pdcsv', *args, **kwargs):
        """
        Create a single appropriate data object using pandas read_csv.

        Args:
            kind (str): One of `pdcsv`_, `pdjson`_, `json`_, `fwf`_
            args: Arguments to be passed to the pandas function
            kwargs: Arguments to be passed to the pandas function

        .. _pdcsv: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
        .. _pdjson: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_json.html
        .. _json: https://docs.python.org/3/library/json.html
        .. _fwf: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_fwf.html
        """
        if kind == "pdcsv":
            return pd.read_csv(self.to_stream(), *args, **kwargs)
        elif kind == "pdjson":
            return pd.read_json(self.to_stream(), *args, **kwargs)
        elif kind == "json":
            return json.load(self.to_stream())
        elif kind == "fwf":
            return pd.read_fwf(self.to_stream(), *args, **kwargs)
        else:
            raise ValueError("Unexpected kind ({})".format(kind))

    def __eq__(self, other):
        if isinstance(other, Editor) and self._lines == other._lines:
            return True
        return False

    def __len__(self):
        return len(self._lines)

    def __iter__(self):
        for line in self._lines:
            yield line

    def __str__(self):
        return '\n'.join(self._lines)

    def __contains__(self, item):
        for obj in self:
            if item in obj:
                return True

    def __delitem__(self, line):
        del self._lines[line]

    def __getitem__(self, key):
        # Getting attribute
        if isinstance(key, six.string_types):
            return getattr(self, key)
        # Slicing a new editor
        kwargs = {'nprint': self.nprint, 'meta': self.meta, 'path_check': False,
                  'encoding': self.encoding, 'as_interned': self.as_interned}
        if isinstance(key, (tuple, list)):
            lines = [self._lines[i] for i in key]
        else:
            lines = self._lines[key]
        return self.__class__(lines, **kwargs)

    def __setitem__(self, line, value):
        self._lines[line] = value

    def __init__(self, data, *args, **kwargs):
        as_interned = kwargs.pop("as_interned", False)
        nprint = kwargs.pop("nprint", 30)
        encoding = kwargs.pop("encoding", "utf-8")
        meta = kwargs.pop("meta", None)
        path_check = kwargs.pop("path_check", True)
        ignore_warning = kwargs.pop("ignore_warning", False)
        super(Editor, self).__init__(*args, **kwargs)
        filepath = None
        if path_check and check_path(data, ignore_warning):
            self._lines = read_file(data, as_interned, encoding)
            filepath = data
        elif isinstance(data, six.string_types):
            self._lines = read_string(data, as_interned)
        elif isinstance(data, (TextIOWrapper, StringIO)):
            self._lines = read_stream(data, as_interned)
        elif isinstance(data, list) and all(isinstance(dat, six.string_types) for dat in data):
            self._lines = data
        elif isinstance(data, Editor):
            self._lines = data._lines
        else:
            raise TypeError("Unknown type for arg data: {}".format(type(data)))
        self.nprint = nprint
        self.as_interned = as_interned
        self.encoding = encoding
        self.meta = meta
        self.cursor = 0
        if filepath is not None:
            try:
                self.meta['filepath'] = filepath
            except TypeError:
                self.meta = {'filepath': filepath}
        else:
            self.meta = {'filepath': None}

    def _html_repr_(self):
        return repr(self)

    def __repr__(self):
        r = ""
        nn = len(self)
        n = len(str(nn))
        if nn > self.nprint * 2:
            for i in range(self.nprint):
                ln = str(i).rjust(n, " ")
                r += self._fmt(ln, self._lines[i])
            r += "...\n".rjust(n, " ")
            for i in range(nn - self.nprint, nn):
                ln = str(i).rjust(n, " ")
                r += self._fmt(ln, self._lines[i])
        else:
            for i, line in enumerate(self):
                ln = str(i).rjust(n, " ")
                r += self._fmt(ln, line)
        return r


def check_path(path, ignore_warning=False):
    """
    Check if path is or looks like a file path (path can be any string data).

    Args:
        path (str): Potential file path
        ignore_warning (bool): Force returning true

    Returns:
        result (bool): True if file path or warning ignored, false otherwise
    """
    try:
        if os.path.exists(path) or (len(path.split("\n")) == 1 and os.sep in path):
            if ignore_warning:
                return False
            return True
    except TypeError:    # Argument ``path`` is not a string file path
        return False


def read_file(path, as_interned=False, encoding="utf-8"):
    """
    Create a list of file lines from a given filepath.

    Interning lines is useful for large files that contain some repeating
    information.

    Args:
        path (str): File path
        as_interned (bool): Memory savings for large repeating text files

    Returns:
        strings (list): File line list
    """
    lines = None
    if path.endswith(".gz"):
        f = gzip.open(path, "rb")
    elif path.endswith(".bz2"):
        f = bz2.open(path, "rb")
    else:
        f = open(path, "rb")
    read = f.read()
    try:
        read = read.decode(encoding)
    except (AttributeError, UnicodeError):
        pass
    if as_interned:
        lines = [sys.intern(line) for line in read.splitlines()]
    else:
        lines = read.splitlines()
    f.close()
    return lines


def read_stream(f, as_interned=False):
    """
    Create a list of file lines from a given file stream.

    Args:
        f (:class:`~io.TextIOWrapper`): File stream
        as_interned (bool): Memory savings for large repeating text files

    Returns:
        strings (list): File line list
    """
    if as_interned:
        return [sys.intern(line) for line in f.read().splitlines()]
    return f.read().splitlines()


def read_string(string, as_interned=False):
    """
    Create a list of file lines from a given string.

    Args:
        string (str): File string
        as_interned (bool): Memory savings for large repeating text files

    Returns:
        strings (list): File line list
    """
    if as_interned:
        return [sys.intern(line) for line in string.splitlines()]
    return string.splitlines()


def concat(*editors, **kwargs):
    """
    Concatenate a collection of editors into a single editor.

    Args:
        editors: Collection of editors (in order) to be concatenated
        kwargs: Arguments for editor creation

    Returns:
        editor: An instance of an editor

    Note:
        Metadata, names, descriptsion, etc. are not automatically propagated.
    """
    return Editor(list(chain(*(ed._lines for ed in editors))), **kwargs)
