# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Editor
####################################
This module provides the :class:`~exa.editor.Editor`, a text manipulation
engine for small/medium sized text files. This class is not a fully fledged
text editor. It provides basic features for searching text (including
regular expressions). This module additionally provides convenience methods
for reading and writing text.
"""
import io, os, re, bz2, six, gzip
import warnings
from io import StringIO, TextIOWrapper
from collections import OrderedDict
from exa.typed import Typed, TypedClass
# Python 2 compatibility
if not hasattr(bz2, "open"):
    bz2.open = bz2.BZ2File


def read_file(path, encoding=None):
    """
    Read in a text file (including compressed text files) to a list of lines.

    .. code-block:: Python

        lines = read_file("myfile.gz")
        lines = read_file("myfile.bz2")
        lines = read_file("myfile.txt")

    Args:
        path (str): File path
        encoding (str): Text encoding

    Returns:
        lines (list): Text lines as list of strings
    """
    if path.endswith(".gz"):
        f = gzip.open(path, "rb")
    elif path.endswith(".bz2"):
        f = bz2.open(path, "rb")
    else:
        f = io.open(path, "rb")
    read = f.read()
    if encoding is not None:
        read = read.decode(encoding)
    else:
        read = read.decode("utf-8", "ignore")
    f.close()
    return read.splitlines()


def write_file(text, path, encoding="utf-8", newline=""):
    """
    Write an editor to a file on disk.

    Args:
        text (str): Text to write
        path (str): Full file path
        encoding (str): File encoding (default utf-8)
        newline (str): Newline delimiter
    """
    with io.open(path, "w", newline=newline, encoding=encoding) as f:
        f.write(six.u(text))


class Editor(TypedClass):
    """
    A text reader object for opening small/medium files on disk.

    The editor can be used to open compressed files (gzip, bz2) directly.
    Editors can write files in a safe manner. Editors can be converted to
    streams in order to facilitate procssing using other tools.

    .. code-block:: python

        ed = Editor(text)
        ed = Editor(myfile)
        ed = Editor(file.gz)
        ed = Editor(file.bz2)

    Args:
        data: File path, text, stream, or archived text file
        nprint (int): Number of lines shown by the 'repr'
        encoding (str): File encoding
        ignore (bool): Ignore file path check (default false)
        cursor (int): Positional search line number
        meta (dict): Dictionary of metadata

    Attributes:
        lines (list):
    """
    meta = Typed(dict, doc="Document metadata")
    lines = Typed(list, doc="Line list")
    cursor = Typed(int, doc="Line number for positional searching.")

    def copy(self):
        """
        Create a copy of the current editor's text.

        Note that this function accepts the same arguments as accepted by the
        :class:`~exa.editor.Editor` object.
        """
        cls = self.__class__
        lines = self.lines[:]
        return cls(lines, ignore=True)

    def format(self, *args, **kwargs):
        """
        Populate the editors templates.

        Templating uses Python's string formatting system.

        Args:
            args: Args for formatting
            kwargs: Kwargs for formatting
            inplace (bool): If True, overwrite editor's contents (default False)

        Returns:
            formatted: Returns the formatted editor (if inplace is False)
        """
        inplace = kwargs.pop("inplace", False)
        if len(args) == len(kwargs) == 0:
            return self
        if inplace:
            self.lines = str(self).format(*args, **kwargs).splitlines()
        else:
            cp = self.copy()
            cp.lines = str(cp).format(*args, **kwargs).splitlines()
            return cp

    def write(self, path, encoding="utf-8", newline="", *args, **kwargs):
        """
        Write editor contents to file.

        Args:
            path (str): Full file path
            args: Positional arguments for formatting
            kwargs: Keyword arguments for formatting

        """
        if len(args) > 0 or len(kwargs) > 0:
            text = str(self.format(*args, **kwargs))
        else:
            text = str(self)
        return write_file(text, path, encoding, newline)

    def find(self, *patterns, **kwargs):
        """
        Search line by line for given patterns.

        Args:
            patterns: String text to search for
            case (bool): Consider character case (default true)

        Returns:
            found (:class:`~exa.core.editor.Found`): Enumerated results
        """
        case = kwargs.pop("case", True)
        if case:
            check = lambda pat, lin: pat in lin
        else:
            patterns = [pattern.lower() for pattern in patterns]
            check = lambda pat, lin: pat in lin.lower()
        patterns = set(patterns)
        matches = OrderedDict([(pattern, []) for pattern in patterns])
        for i, line in enumerate(self):
            for pattern in patterns:
                if check(pattern, line):
                    matches[pattern].append((i, line))
        return matches

    def replace(self, pattern, replacement, inplace=False):
        """
        Replace a pattern with some text.

        Args:
            pattern (str): Pattern to replace
            replacement (str): Value for replacement
            inplace (bool): Perform replacement in place
        """
        if inplace:
            for i in range(len(self)):
                self.line[i] = self.line[i].replace(pattern, replacement)
        else:
            lines = []
            for line in self:
                lines.append(line.replace(pattern, replacement))
            return self.__class__(lines)

    def find_next(self, *patterns, case=True, reverse=False, wrap=False, cursor=None):
        """
        Find the next line with the given text pattern.

        If no match is found, none is returned. If a match is found, the cursor
        position is updated and a tuple of line number and text is returned.

        Args:
            pattern (str): String pattern to search for
            case (bool): Respect case
            reverse (bool): Search in reverse
            cursor (int): Set the line cursor prior to search (optional)
        """
        positions = self._next_positions(wrap, reverse, cursor)
        if case:
            check = lambda lin: any(pattern in lin for pattern in patterns)
        else:
            patterns = [p.lower() for p in patterns]
            check = lambda lin: any(pattern in lin.lower() for pattern in patterns)
        patterns = set(patterns)
        for start, stop, inc in positions:
            for i in range(start, stop, inc):
                if check(self.lines[i]):
                    self.cursor = i
                    return i, self.lines[i]

    def regex(self, *patterns, **kwargs):
        """
        Search text for specific regular expressions (line by line).

        .. code-block:: python

            ed = Editor(text)
            found = ed.regex("[a-z0-9]", re.compile("text\nother", re.MULTILINE))

        Args:
            patterns: Regular expressions
            flags: Python regular expression flags

        Returns:
            found (:class:`~exa.core.editor.Found`): Enumerated results
        """
        flags = kwargs.pop("flags", re.DOTALL)
        regexes = []
        for p in patterns:
            if type(p).__name__ != "SRE_Pattern":    # Compiled regex type check
                reg = re.compile(p, flags)
                if p not in [r.pattern for r in regexes]:
                    regexes.append(reg)
            elif p.pattern not in [r.pattern for r in regexes]:
                regexes.append(p)
        regexes = set(regexes)
        matches = OrderedDict([(r.pattern, []) for r in regexes])
        #char_cum_sum = np.cumsum(list(map(len, self.lines)))
        for i, line in enumerate(self):
            for regex in regexes:
                if regex.search(line):
                    matches[regex.pattern].append((i, line))
        return matches

    def regex_next(self, *patterns, flags=0, reverse=False, wrap=False, cursor=None):
        """
        Find the next line with a given regular expression pattern.

        If no matches are found, None is returned. Certain flags (such as
        multiline) are not supported by this function.

        Args:
            pattern (regex): Regular expression to search for
            flags (int): Regularexpression compilation flags
            reverse (bool): Search backwards
            wrap (bool): Continue search from beginning/end of file (wraparound end of file)
            cursor (int): Set the cursor prior to searching
        """
        positions = self._next_positions(wrap, reverse, cursor)
        regexes = []
        for p in patterns:
            if type(p).__name__ != "SRE_Pattern":    # Compiled regex type check
                reg = re.compile(p, flags)
                if p not in [r.pattern for r in regexes]:
                    regexes.append(reg)
            elif p.pattern not in [r.pattern for r in regexes]:
                regexes.append(p)
        regexes = set(regexes)
        for start, stop, inc in positions:
            for i in range(start, stop, inc):
                for regex in regexes:
                    if regex.search(self.lines[i]):
                        self.cursor = i
                        return i, self.lines[i]

    def _next_positions(self, wrap=False, reverse=False, cursor=None):
        """
        Helper function that correctly gets the positions to search
        for the find_next and regex_next functions. The returned tuple
        are arguments for ``range``.

        See Also:
            :func:`~exa.core.editor.find_next`,
            :func:`~exa.core.editor.regex_next`
        """
        n = len(self)
        n1 = n - 1
        # Set the cursor
        if cursor is not None:
            self.cursor = cursor
        while True:
            if self.cursor > n1:
                self.cursor -= n
            elif self.cursor < 0:
                self.cursor += n
            else:
                break
        # Determine how the searching positions should go
        if wrap == False and reverse == False:
            # Search from the cursor + 1 until the end of the file.
            self.cursor = 0 if self.cursor == n1 else self.cursor + 1
            positions = ((self.cursor, n, 1), )
        elif wrap == False and reverse == True:
            # Search from the cursor - 1 until the beginning of the file.
            self.cursor = n1 if self.cursor == 0 else self.cursor - 1
            positions = ((self.cursor, 0, -1), )
        elif wrap == True and reverse == False:
            # Search from the cursor + 1 until the end of the file and then
            # continue from the beginning until the original cursor position.
            self.cursor = 0 if self.cursor == n1 else self.cursor + 1
            positions = ((self.cursor, n, 1), (0, self.cursor, 1))
        else:
            # Search from the cursor - 1 until the beginning of the file
            # and then continue from the end of the file until the original
            # cursor position.
            self.cursor = n1 if self.cursor == 0 else self.cursor - 1
            positions = ((self.cursor, 0, -1), (n1, self.cursor, -1))
        return positions

    def to_stream(self):
        """Return a stream object of the current editor."""
        return StringIO(six.u(str(self)))

    def __iter__(self):
        for line in self.lines:
            yield line

    def __contains__(self, text):
        if not isinstance(text, six.string_types):
            text = str(text)
        # Use __iter__
        for line in self:
            if text in line:
                return True
        return False

    def __delitem__(self, line):
        del self.lines[line]

    def __getitem__(self, key):
        # The following makes a copy
        cls = self.__class__
        if isinstance(key, (tuple, list)):
            lines = [self.lines[i] for i in key]
        else:
            lines = self.lines[key]
        return cls(textobj=lines, ignore=True)

    def __setitem__(self, line, value):
        self.lines[line] = value

    def __str__(self):
        return "\n".join(self.lines)

    def __len__(self):
        return len(self.lines)

    def __init__(self, textobj, encoding=None, nprint=15, ignore=False):
        """
        Check if accidental filepath but missing file or wrong directory.
        Warn the user unless ignore is true.
        """
        if (isinstance(textobj, six.string_types) and
            os.path.sep in textobj and len(textobj.split("\n")) == 1
            and ignore == False and not os.path.exists(textobj)):
            warnings.warn("Possibly incorrect file path! {}".format(textobj))
        if isinstance(textobj, str) and os.path.exists(textobj):
            lines = read_file(textobj, encoding=encoding)
        elif isinstance(textobj, six.string_types):
            lines = str(textobj).splitlines()
        elif isinstance(textobj, (list, tuple)) and isinstance(textobj[0], six.string_types):
            lines = textobj
        elif isinstance(textobj, (TextIOWrapper, StringIO)):
            lines = textobj.read().splitlines()
        elif isinstance(textobj, Editor):
            lines = textobj.lines
        else:
            raise TypeError("Object of type {} not supported by Editors.".format(type(textobj)))
        self.lines = lines
        self.cursor = 0
        self.nprint = nprint

    def __repr__(self):
        r = ""
        nn = len(self)
        n = len(str(nn))
        fmt = lambda x, y: " "*(n-len(str(x))) + "{0}: {1}".format(x, y)
        if nn > 2*self.nprint:
            r += "\n".join(map(fmt, range(self.nprint), self.lines[:self.nprint]))
            r += "\n" + "."*n + "\n"
            r += "\n".join(map(fmt, range(nn-self.nprint, nn), self.lines[-self.nprint:]))
        else:
            r += "\n".join(map(fmt, range(len(self)), self.lines))
        return r






#import os, re, sys, bz2, gzip, six, json
#import pandas as pd
#from copy import copy, deepcopy
#from collections import defaultdict
#from itertools import chain
#from io import StringIO, TextIOWrapper
#from IPython.display import display
#from .base import Base
#from exa import TypedProperty
#from exa.typed import yield_typed
#if not hasattr(bz2, "open"):
#    bz2.open = bz2.BZ2File
#
#
#@typed
#class Editor(object):
#    """
#    An in memory representation of a text file.
#
#    The editor can be used to quickly and efficiently convert text data
#    to Python objects such as ints, floats, lists, arrays, etc.
#
#    Args:
#        data: File path, text, stream, or archived text file
#        nprint (int): Number of lines shown by the 'repr'
#        encoding (str): File encoding
#        meta (dict): Metadata
#        path_check (bool): Force file path check (default true)
#        ignore_warning (bool): Ignore file path warning (default false)
#
#    Attributes:
#        cursor (int): Cursor position (line number)
#        _fmt (str): Format string for display ('repr')
#        _tmpl (str): Regex for identifying templates
#
#    See Also:
#        :class:`~exa.core.composer.Compser`s are useful for building text
#        files programmatically. The :mod:`~exa.core.parser` module provides
#        classes useful for programatic parsing of text files.
#    """
#    _fmt = "{0}: {1}\n".format
#    _tmpl = "{.*?}"
#    meta = TypedProperty(dict, "Editor metadata")
#
#    @property
#    def templates(self):
#        """
#        Display a list of Python string templates present in this text.
#
#        .. code-block:: text
#
#            tmpl = "this is a {template}"
#            tmpl.format(template="other text")    # prints "this is a other text"
#
#        See Also:
#            `String formatting`_.
#
#        .. _String formatting: https://docs.python.org/3.6/library/string.html
#        """
#        return [match[1:-1] for match in self.regex(self._tmpl, num=False)[self._tmpl] if not match.startswith("{{")]
#
#    @property
#    def constants(self):
#        """
#        Display test of literal curly braces.
#
#        .. code-block:: text
#
#            cnst = "this is a {{constant}}"   # Cannot be "formatted"
#
#        See Also:
#            `String formatting`_.
#
#        .. _String formatting: https://docs.python.org/3.6/library/string.html
#        """
#        return [match[2:-1] for match in self.regex(self._tmpl, num=False)[self._tmpl] if match.startswith("{{")]
#
#    def regex(self, *patterns, **kwargs):
#        """
#        Match a line or lines by the specified regular expression(s).
#
#        Returned values may be a list of (number, text) pairs or a list of line
#        numbers or a list of text strings.
#
#        .. code-block:: python
#
#            ed = Editor(text)
#            ed.regex("^=+$")            # Returns (line number, text) pairs where the line contains only '='
#            ed.regex("^=+$", "find")    # Search for multiple regex simultaneously
#
#        Args:
#            patterns: Regular expressions
#            num (bool): Return line number (default true)
#            text (bool): Return line text (default true)
#            flags: Python regex flags (default re.MULTILINE)
#
#        Returns:
#            results (dict): Dictionary with pattern keys and list of values
#
#        Note:
#            By default, regular expression search multiple lines (``re.MULTILINE``).
#
#        See Also:
#            https://en.wikipedia.org/wiki/Regular_expression
#        """
#        num = kwargs.pop("num", True)
#        text = kwargs.pop("text", True)
#        flags = kwargs.pop('flags', re.MULTILINE)
#        results = defaultdict(list)
#        self_str = str(self)
#        for pattern in patterns:
#            match = pattern
#            if not type(pattern).__name__ == "SRE_Pattern":    # Compiled regular expression type check
#                match = re.compile(pattern, flags)
#            if num and text:
#                for m in match.finditer(self_str):
#                    results[match.pattern].append((self_str.count("\n", 0, m.start()) + 1, m.group()))
#            elif num:
#                for m in match.finditer(self_str):
#                    results[match.pattern].append(self_str.count("\n", 0, m.start()) + 1)
#            elif text:
#                for m in match.finditer(self_str):
#                    results[match.pattern].append(m.group())
#            else:
#                raise ValueError("At least one of ``num`` or ``text`` must be true.")
#        return results
#
#    def find(self, *patterns, **kwargs):
#        """
#        Search for patterns line by line.
#
#        Args:
#            strings (str): Any number of strings to search for
#            case (bool): Check case (default true)
#            num (bool): Return line number (default true)
#            text (bool): Return line text (default true)
#
#        Returns:
#            results (dict): Dictionary with pattern keys and list of (lineno, line) values
#        """
#        num = kwargs.pop("num", True)
#        text = kwargs.pop("text", True)
#        case = kwargs.pop("case", True)
#        results = defaultdict(list)
#        for i, line in enumerate(self):
#            for pattern in patterns:
#                if case:
#                    check = pattern in line
#                else:
#                    check = pattern.lower() in line.lower()
#                if check:
#                    if num and text:
#                        results[pattern].append((i, line))
#                    elif num:
#                        results[pattern].append(i)
#                    elif text:
#                        results[pattern].append(line)
#                    else:
#                        raise ValueError("At least one of ``num`` or ``text`` must be true.")
#        return results
#
#    def find_next(self, pattern, num=True, text=True, reverse=False):
#        """
#        From the current cursor position, find the next occurrence of the pattern.
#
#        Args:
#            pattern (str): String to search for from the cursor
#            num (bool): Return line number (default true)
#            text (bool): Return line text (default true)
#            reverse (bool): Find next in reverse (default false)
#
#        Returns:
#            tup (tuple): Tuple of line number and line of next occurrence
#
#        Note:
#            Searching will cycle the file and continue if an occurrence is not
#            found (forward or reverse direction determined by ``reverse``).
#        """
#        n = len(self)
#        n1 = n - 1
#        if reverse:
#            self.cursor = 0 if self.cursor == 0 else self.cursor - 1
#            positions = [(self.cursor - 1, 0, -1), (n1, self.cursor, -1)]
#        else:
#            self.cursor = 0 if self.cursor == n1 else self.cursor + 1
#            positions = [(self.cursor, n, 1), (0, self.cursor, 1)]
#        for start, stop, inc in positions:
#            for i in range(start, stop, inc):
#                if pattern in str(self[i]):
#                    self.cursor = i
#                    if num and text:
#                        return (i, str(self[i]))
#                    elif num:
#                        return i
#                    elif text:
#                        return str(self[i])
#                    else:
#                        raise ValueError("At least one of ``num`` or ``text`` must be true.")
#
#    def copy(self):
#        """Return a copy of the current editor."""
#        special = ("_lines", "as_interned", "nprint", "meta", "encoding")
#        cls = self.__class__
#        lines = self._lines[:]
#        as_interned = copy(self.as_interned)
#        nprint = copy(self.nprint)
#        meta = deepcopy(self.meta)
#        encoding = copy(self.encoding)
#        cp = {k: copy(v) for k, v in self._vars(True).items() if k not in special}
#        return cls(lines, as_interned, nprint, meta, encoding, **cp)
#
#    def format(self, *args, **kwargs):
#        """
#        Populate the editors templates.
#
#        Args:
#            args: Args for formatting
#            kwargs: Kwargs for formatting
#            inplace (bool): If True, overwrite editor's contents (default False)
#
#        Returns:
#            formatted: Returns the formatted editor (if inplace is False)
#        """
#        inplace = kwargs.pop("inplace", False)
#        if inplace:
#            self._lines = str(self).format(*args, **kwargs).splitlines()
#        else:
#            cp = self.copy()
#            cp._lines = str(cp).format(*args, **kwargs).splitlines()
#            return cp
#
#    def write(self, path, *args, **kwargs):
#        """
#        Write the editor contents to a file.
#
#        Args:
#            path (str): Full file path (default none, prints to stdout)
#            args: Positional arguments for formatting
#            kwargs: Keyword arguments for formatting
#        """
#        with open(path, "wb") as f:
#            if len(args) > 0 or len(kwargs) > 0:
#                f.write(six.b(str(self.format(*args, **kwargs))))
#            else:
#                f.write(six.b(str(self)))
#
#    def head(self, n=10):
#        """Display the top of the file."""
#        return "\n".join(self._lines[:n])
#
#    def tail(self, n=10):
#        """Display the bottom of the file."""
#        return "\n".join(self._lines[-n:])
#
#    def append(self, lines):
#        """
#        Append lines to the editor.
#
#        Args:
#            lines (list, str): List of lines or text to append to the editor
#
#        Note:
#            Occurs in-place, like ``list.append``.
#        """
#        if isinstance(lines, list):
#            self._lines += lines
#        elif isinstance(lines, six.string_types):
#            self._lines += lines.splitlines()
#        else:
#            raise TypeError("Unsupported type {} for lines.".format(type(lines)))
#
#    def prepend(self, lines):
#        """
#        Prepend lines to the editor.
#
#        Args:
#            lines (list, str): List of lines or text to append to the editor
#
#        Note:
#            Occurs in-place, like ``list.insert(0, ...)``.
#        """
#        if isinstance(lines, list):
#            self._lines = lines + self._lines
#        elif isinstance(lines, six.string_types):
#            self._lines = lines.splitlines() + self._lines
#        else:
#            raise TypeError("Unsupported type {} for lines.".format(type(lines)))
#
#    def insert(self, lineno, lines):
#        """
#        Insert lines into the editor after ``lineno``.
#
#        Args:
#            num (int): Line number after which to insert lines
#            text (list, str): List of lines or text to append to the editor
#
#        Note:
#            Occurs in-place, like ``list.insert(...)``.
#        """
#        if isinstance(lines, six.string_types):
#            lines = lines.splitlines()
#        elif not isinstance(lines, list):
#            raise TypeError("Unsupported type {} for lines.".format(type(lines)))
#        self._lines = self._lines[:lineno] + lines + self._lines[lineno:]
#
#    def replace(self, pattern, replacement, inplace=False):
#        """
#        Replace all instances of a pattern with a replacement.
#
#        Args:
#            pattern (str): Pattern to replace
#            replacement (str): Text to insert
#
#        """
#        lines = []
#        for line in self:
#            lines.append(line.replace(pattern, replacement))
#        if inplace:
#            self._lines = lines
#        else:
#            new = self.copy()
#            new._lines = lines
#            return new
#
#    def remove_blank_lines(self):
#        """Remove all blank lines (blank lines are those with zero characters)."""
#        to_remove = []
#        for i, line in enumerate(self):
#            ln = line.strip()
#            if ln == '':
#                to_remove.append(i)
#        self.delete_lines(to_remove)
#
#    def delete_lines(self, lines):
#        """
#        Delete all lines with given line numbers.
#
#        Args:
#            lines (list): List of integers corresponding to line numbers to delete
#        """
#        for k, i in enumerate(sorted(lines)):
#            del self[i-k]
#
#    def iterlines(self, start=0, stop=None, step=None):
#        """Line generator."""
#        for line in self._lines[slice(start, stop, step)]:
#            yield line
#
#    def info(self, df=False):
#        """
#        Describe the current editor and its data objects.
#
#        Args:
#            df (bool): If true, returns the full dataframe
#        """
#        l = len(self)
#        f = self.meta['filepath'] if self.meta is not None and "filepath" in self.meta else "NA"
#        print("Basic Info:\n    file length: {0}\n    file name: {1}".format(l, f))
#        names = []
#        types = []
#        docs = []
#        for name, _ in yield_typed(self):
#            attr = getattr(self, name)
#            names.append(name)
#            types.append(type(attr))
#            docs.append(attr.__doc__)
#        df_ = pd.DataFrame.from_dict({'name': names, 'data_type': types, 'docs': docs}).set_index('name')
#        display(df_)
#        if df:
#            return df_
#
#    def to_file(self, path, *args, **kwargs):
#        """Convenience name for :func:`~exa.core.editor.Editor.write`."""
#        self.write(path, *args, **kwargs)
#
#    def to_data(self, kind='pdcsv', *args, **kwargs):
#        """
#        Create a single appropriate data object using pandas read_csv.
#
#        Args:
#            kind (str): One of `pdcsv`_, `pdjson`_, `json`_, `fwf`_
#            args: Arguments to be passed to the pandas function
#            kwargs: Arguments to be passed to the pandas function
#
#        .. _pdcsv: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
#        .. _pdjson: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_json.html
#        .. _json: https://docs.python.org/3/library/json.html
#        .. _fwf: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_fwf.html
#        """
#        if kind == "pdcsv":
#            return pd.read_csv(self.to_stream(), *args, **kwargs)
#        elif kind == "pdjson":
#            return pd.read_json(self.to_stream(), *args, **kwargs)
#        elif kind == "json":
#            return json.load(self.to_stream())
#        elif kind == "fwf":
#            return pd.read_fwf(self.to_stream(), *args, **kwargs)
#        else:
#            raise ValueError("Unexpected kind ({})".format(kind))
#
#    def __eq__(self, other):
#        if isinstance(other, Editor) and self._lines == other._lines:
#            return True
#        return False
#
#    def __len__(self):
#        return len(self._lines)
#
#    def __iter__(self):
#        for line in self._lines:
#            yield line
#
#    def __str__(self):
#        return '\n'.join(self._lines)
#
#    def __contains__(self, item):
#        for obj in self:
#            if item in obj:
#                return True
#
#    def __delitem__(self, line):
#        del self._lines[line]
#
#    def __getitem__(self, key):
#        # Getting attribute
#        if isinstance(key, six.string_types):
#            return getattr(self, key)
#        # Slicing a new editor
#        kwargs = {'nprint': self.nprint, 'meta': self.meta, 'path_check': False,
#                  'encoding': self.encoding, 'as_interned': self.as_interned}
#        if isinstance(key, (tuple, list)):
#            lines = [self._lines[i] for i in key]
#        else:
#            lines = self._lines[key]
#        return self.__class__(lines, **kwargs)
#
#    def __setitem__(self, line, value):
#        self._lines[line] = value
#
#    def __init__(self, data, *args, **kwargs):
#        as_interned = kwargs.pop("as_interned", False)
#        nprint = kwargs.pop("nprint", 30)
#        encoding = kwargs.pop("encoding", "utf-8")
#        meta = kwargs.pop("meta", None)
#        path_check = kwargs.pop("path_check", True)
#        ignore_warning = kwargs.pop("ignore_warning", False)
#        super(Editor, self).__init__(*args, **kwargs)
#        filepath = None
#        if path_check and check_path(data, ignore_warning):
#            self._lines = read_file(data, as_interned, encoding)
#            filepath = data
#        elif isinstance(data, six.string_types):
#            self._lines = read_string(data, as_interned)
#        elif isinstance(data, (TextIOWrapper, StringIO)):
#            self._lines = read_stream(data, as_interned)
#        elif isinstance(data, list) and all(isinstance(dat, six.string_types) for dat in data):
#            self._lines = data
#        elif isinstance(data, Editor):
#            self._lines = data._lines
#        else:
#            raise TypeError("Unknown type for arg data: {}".format(type(data)))
#        self.nprint = nprint
#        self.as_interned = as_interned
#        self.encoding = encoding
#        self.meta = meta
#        self.cursor = 0
#        if filepath is not None:
#            try:
#                self.meta['filepath'] = filepath
#            except TypeError:
#                self.meta = {'filepath': filepath}
#        else:
#            self.meta = {'filepath': None}
#
#    def __repr__(self):
#        r = ""
#        nn = len(self)
#        n = len(str(nn))
#        if nn > self.nprint * 2:
#            for i in range(self.nprint):
#                ln = str(i).rjust(n, " ")
#                r += self._fmt(ln, self._lines[i])
#            r += "...\n".rjust(n, " ")
#            for i in range(nn - self.nprint, nn):
#                ln = str(i).rjust(n, " ")
#                r += self._fmt(ln, self._lines[i])
#        else:
#            for i, line in enumerate(self):
#                ln = str(i).rjust(n, " ")
#                r += self._fmt(ln, line)
#        return r
#
#
#def check_path(path, ignore_warning=False):
#    """
#    Check if path is or looks like a file path (path can be any string data).
#
#    Args:
#        path (str): Potential file path
#        ignore_warning (bool): Force returning true
#
#    Returns:
#        result (bool): True if file path or warning ignored, false otherwise
#    """
#    try:
#        if os.path.exists(path) or (len(path.split("\n")) == 1 and os.sep in path):
#            if ignore_warning:
#                return False
#            return True
#    except TypeError:    # Argument ``path`` is not a string file path
#        return False
#
#
#def read_file(path, as_interned=False, encoding="utf-8"):
#    """
#    Create a list of file lines from a given filepath.
#
#    Interning lines is useful for large files that contain some repeating
#    information.
#
#    Args:
#        path (str): File path
#        as_interned (bool): Memory savings for large repeating text files
#
#    Returns:
#        strings (list): File line list
#    """
#    lines = None
#    if path.endswith(".gz"):
#        f = gzip.open(path, "rb")
#    elif path.endswith(".bz2"):
#        f = bz2.open(path, "rb")
#    else:
#        f = open(path, "rb")
#    read = f.read()
#    try:
#        read = read.decode(encoding)
#    except (AttributeError, UnicodeError):
#        pass
#    if as_interned:
#        lines = [sys.intern(line) for line in read.splitlines()]
#    else:
#        lines = read.splitlines()
#    f.close()
#    return lines
#
#
#def read_stream(f, as_interned=False):
#    """
#    Create a list of file lines from a given file stream.
#
#    Args:
#        f (:class:`~io.TextIOWrapper`): File stream
#        as_interned (bool): Memory savings for large repeating text files
#
#    Returns:
#        strings (list): File line list
#    """
#    if as_interned:
#        return [sys.intern(line) for line in f.read().splitlines()]
#    return f.read().splitlines()
#
#
#def read_string(string, as_interned=False):
#    """
#    Create a list of file lines from a given string.
#
#    Args:
#        string (str): File string
#        as_interned (bool): Memory savings for large repeating text files
#
#    Returns:
#        strings (list): File line list
#    """
#    if as_interned:
#        return [sys.intern(line) for line in string.splitlines()]
#    return string.splitlines()
#
#
#def concat(*editors, **kwargs):
#    """
#    Concatenate a collection of editors into a single editor.
#
#    Args:
#        editors: Collection of editors (in order) to be concatenated
#        kwargs: Arguments for editor creation
#
#    Returns:
#        editor: An instance of an editor
#
#    Note:
#        Metadata, names, descriptsion, etc. are not automatically propagated.
#    """
#    return Editor(list(chain(*(ed._lines for ed in editors))), **kwargs)
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
#"""
#Editor
#####################################
#Text-editor-like functionality for programatically manipulating raw text input
#and output data and converting this data into container objects. This class
#does not behave like a fully fledged text editor but does have some basic find,
#replace, insert, etc. functionality.
#"""
#from __future__ import print_function
#import io, os, re, sys, six
#import pandas as pd
#import warnings
#
#
#class Editor(object):
#    """
#    An editor is a representation of a text file on disk that can be
#    programmatically manipulated.
#
#    Text lines are stored in memory; no files remain open. This class does not
#    strive to be a fully fledged text editor rather a base class for converting
#    input and output data from text on disk to some type of (exa framework)
#    container object (and vice versa).
#
#    >>> template = "Hello World!\\nHello {user}"
#    >>> editor = Editor(template)
#    >>> editor[0]
#    'Hello World!'
#    >>> len(editor)
#    2
#    >>> del editor[0]
#    >>> len(editor)
#    1
#    >>> editor.write(fullpath=None, user='Alice')
#    Hello Alice
#
#    Tip:
#        Editor line numbers use a 0 base index. To increase the number of lines
#        displayed by the repr, increase the value of the **nprint** attribute.
#
#    Warning:
#        For large text with repeating strings be sure to use the **as_interned**
#        argument.
#
#    Attributes:
#        name (str): Data/file/misc name
#        description (str): Data/file/misc description
#        meta (dict): Additional metadata as key, value pairs
#        nrpint (int): Number of lines to display when printing
#        cursor (int): Line number position of the cusor (see :func:`~exa.core.editor.Editor.find_next`)
#    """
#    _getter_prefix = 'parse'
#    _fmt = '{0}: {1}\n'.format   # Format for printing lines (see __repr__)
#
#    def write(self, path=None, *args, **kwargs):
#        """
#        Perform formatting and write the formatted string to a file or stdout.
#
#        Optional arguments can be used to format the editor's contents. If no
#        file path is given, prints to standard output.
#
#        Args:
#            path (str): Full file path (default None, prints to stdout)
#            *args: Positional arguments to format the editor with
#            **kwargs: Keyword arguments to format the editor with
#        """
#        if path is None:
#            print(self.format(*args, **kwargs))
#        else:
#            with io.open(path, 'w', newline="") as f:
#                f.write(self.format(*args, **kwargs))
#
#    def format(self, *args, **kwargs):
#        """
#        Format the string representation of the editor.
#
#        Args:
#            inplace (bool): If True, overwrite editor's contents with formatted contents
#        """
#        inplace = kwargs.pop("inplace", False)
#        if not inplace:
#            return str(self).format(*args, **kwargs)
#        self._lines = str(self).format(*args, **kwargs).splitlines()
#
#    def head(self, n=10):
#        """
#        Display the top of the file.
#
#        Args:
#            n (int): Number of lines to display
#        """
#        r = self.__repr__().split('\n')
#        print('\n'.join(r[:n]), end=' ')
#
#    def tail(self, n=10):
#        """
#        Display the bottom of the file.
#
#        Args:
#            n (int): Number of lines to display
#        """
#        r = self.__repr__().split('\n')
#        print('\n'.join(r[-n:]), end=' ')
#
#    def append(self, lines):
#        """
#        Args:
#            lines (list): List of line strings to append to the end of the editor
#        """
#        if isinstance(lines, list):
#            self._lines = self._lines + lines
#        elif isinstance(lines, str):
#            lines = lines.split('\n')
#            self._lines = self._lines + lines
#        else:
#            raise TypeError('Unsupported type {0} for lines.'.format(type(lines)))
#
#    def prepend(self, lines):
#        """
#        Args:
#            lines (list): List of line strings to insert at the beginning of the editor
#        """
#        if isinstance(lines, list):
#            self._lines = lines + self._lines
#        elif isinstance(lines, str):
#            lines = lines.split('\n')
#            self._lines = lines + self._lines
#        else:
#            raise TypeError('Unsupported type {0} for lines.'.format(type(lines)))
#
#    def insert(self, lines=None):
#        """
#        Insert lines into the editor.
#
#        Note:
#            To insert before the first line, use :func:`~exa.core.editor.Editor.preappend`
#            (or key 0); to insert after the last line use :func:`~exa.core.editor.Editor.append`.
#
#        Args:
#            lines (dict): Dictionary of lines of form (lineno, string) pairs
#        """
#        for i, (key, line) in enumerate(lines.items()):
#            n = key + i
#            first_half = self._lines[:n]
#            last_half = self._lines[n:]
#            self._lines = first_half + [line] + last_half
#
#    def remove_blank_lines(self):
#        """Remove all blank lines (blank lines are those with zero characters)."""
#        to_remove = []
#        for i, line in enumerate(self):
#            ln = line.strip()
#            if ln == '':
#                to_remove.append(i)
#        self.delete_lines(to_remove)
#
#    def _data(self, copy=False):
#        """
#        Get all data associated with the container as key value pairs.
#        """
#        data = {}
#        for key, obj in self.__dict__.items():
#            if isinstance(obj, (pd.Series, pd.DataFrame, pd.SparseSeries, pd.SparseDataFrame)):
#                if copy:
#                    data[key] = obj.copy()
#                else:
#                    data[key] = obj
#        return data
#
#    def delete_lines(self, lines):
#        """
#        Delete all lines with given line numbers.
#
#        Args:
#            lines (list): List of integers corresponding to line numbers to delete
#        """
#        for k, i in enumerate(lines):
#            del self[i-k]    # Accounts for the fact that len(self) decrease upon deletion
#
#    def find(self, *strings, **kwargs):
#        """
#        Search the entire editor for lines that match the string.
#
#        .. code-block:: Python
#
#            string = '''word one
#            word two
#            three'''
#            ed = Editor(string)
#            ed.find('word')          # [(0, "word one"), (1, "word two")]
#            ed.find('word', 'three') # {'word': [...], 'three': [(2, "three")]}
#
#        Args:
#            strings (str): Any number of strings to search for
#            keys_only (bool): Only return keys
#            start (int): Optional line to start searching on
#            stop (int): Optional line to stop searching on
#
#        Returns:
#            results: If multiple strings searched a dictionary of string key, (line number, line) values (else just values)
#        """
#        start = kwargs.pop("start", 0)
#        stop = kwargs.pop("stop", None)
#        keys_only = kwargs.pop("keys_only", False)
#        results = {string: [] for string in strings}
#        stop = len(self) if stop is None else stop
#        for i, line in enumerate(self[start:stop]):
#            for string in strings:
#                if string in line:
#                    if keys_only:
#                        results[string].append(i)
#                    else:
#                        results[string].append((i, line))
#        if len(strings) == 1:
#            return results[strings[0]]
#        return results
#
#    def find_next(self, *strings, **kwargs):
#        """
#        From the editor's current cursor position find the next instance of the
#        given string.
#
#        Args:
#            strings (iterable): String or strings to search for
#
#        Returns:
#            tup (tuple): Tuple of cursor position and line or None if not found
#
#        Note:
#            This function cycles the entire editor (i.e. cursor to length of
#            editor to zero and back to cursor position).
#        """
#        start = kwargs.pop("start", None)
#        keys_only = kwargs.pop("keys_only", False)
#        staht = start if start is not None else self.cursor
#        for start, stop in [(staht, len(self)), (0, staht)]:
#            for i in range(start, stop):
#                for string in strings:
#                    if string in self[i]:
#                        tup = (i, self[i])
#                        self.cursor = i + 1
#                        if keys_only: return i
#                        return tup
#
#    def regex(self, *patterns, **kwargs):
#        """
#        Search the editor for lines matching the regular expression.
#        re.MULTILINE is not currently supported.
#
#        Args:
#            \*patterns: Regular expressions to search each line for
#            keys_only (bool): Only return keys
#            flags (re.FLAG): flags passed to re.search
#
#        Returns:
#            results (dict): Dictionary of pattern keys, line values (or groups - default)
#        """
#        start = kwargs.pop("start", 0)
#        stop = kwargs.pop("stop", None)
#        keys_only = kwargs.pop("keys_only", False)
#        flags = kwargs.pop("flags", 0)
#        results = {pattern: [] for pattern in patterns}
#        stop = stop if stop is not None else -1
#        for i, line in enumerate(self[start:stop]):
#            for pattern in patterns:
#                grps = re.search(pattern, line, flags=flags)
#                if grps and keys_only:
#                    results[pattern].append(i)
#                elif grps and grps.groups():
#                    for group in grps.groups():
#                        results[pattern].append((i, group))
#                elif grps:
#                    results[pattern].append((i, line))
#        if len(patterns) == 1:
#            return results[patterns[0]]
#        return results
#
#    def replace(self, pattern, replacement):
#        """
#        Replace all instances of a pattern with a replacement.
#
#        Args:
#            pattern (str): Pattern to replace
#            replacement (str): Text to insert
#        """
#        for i in range(len(self)):
#            line = self[i]
#            while pattern in line:
#                line = line.replace(pattern, replacement)
#            self[i] = line
#
#    def pandas_dataframe(self, start, stop, ncol, **kwargs):
#        """
#        Returns the result of tab-separated pandas.read_csv on
#        a subset of the file.
#
#        Args:
#            start (int): line number where structured data starts
#            stop (int): line number where structured data stops
#            ncol (int or list): the number of columns in the structured
#                data or a list of that length with column names
#
#        Returns:
#            pd.DataFrame: structured data
#        """
#        try:
#            int(start)
#            int(stop)
#        except:
#            print('start and stop must be ints')
#        try:
#            ncol = int(ncol)
#            return pd.read_csv(io.StringIO('\n'.join(self[start:stop])), delim_whitespace=True, names=range(ncol), **kwargs)
#        except TypeError:
#            try:
#                ncol = list(ncol)
#                return pd.read_csv(io.StringIO('\n'.join(self[start:stop])), delim_whitespace=True, names=ncol, **kwargs)
#            except TypeError:
#                print('Cannot pandas_dataframe if ncol is {}, must be int or list'.format(type(ncol)))
#
#
#    @property
#    def variables(self):
#        """
#        Display a list of templatable variables present in the file.
#
#        Templating is accomplished by creating a bracketed object in the same
#        way that Python performs `string formatting`_. The editor is able to
#        replace the placeholder value of the template. Integer templates are
#        positional arguments.
#
#        .. _string formatting: https://docs.python.org/3.6/library/string.html
#        """
#        string = str(self)
#        constants = [match[1:-1] for match in re.findall('{{[A-z0-9]}}', string)]
#        variables = re.findall('{[A-z0-9]*}', string)
#        return sorted(set(variables).difference(constants))
#
#    @classmethod
#    def from_file(cls, path, **kwargs):
#        """Create an editor instance from a file on disk."""
#        lines = lines_from_file(path)
#        if 'meta' not in kwargs:
#            kwargs['meta'] = {'from': 'file'}
#        kwargs['meta']['filepath'] = path
#        return cls(lines, **kwargs)
#
#    @classmethod
#    def from_stream(cls, f, **kwargs):
#        """Create an editor instance from a file stream."""
#        lines = lines_from_stream(f)
#        if 'meta' not in kwargs:
#            kwargs['meta'] = {'from': 'stream'}
#        kwargs['meta']['filepath'] = f.name if hasattr(f, 'name') else None
#        return cls(lines, **kwargs)
#
#    @classmethod
#    def from_string(cls, string, **kwargs):
#        """Create an editor instance from a string template."""
#        return cls(lines_from_string(string), **kwargs)
#
#    def __init__(self, path_stream_or_string, as_interned=False, nprint=30,
#                 name=None, description=None, meta=None, encoding=None, ignore=False):
#        # Backporting file check
#        textobj = path_stream_or_string
#        if (isinstance(textobj, six.string_types) and len(textobj.split("\n")) == 1
#            and ignore == False and not os.path.exists(textobj)):
#            warnings.warn("Possibly incorrect file path! {}".format(textobj))
#        #
#        if len(path_stream_or_string) < 256 and os.path.exists(path_stream_or_string):
#            self._lines = lines_from_file(path_stream_or_string, as_interned, encoding)
#        elif isinstance(path_stream_or_string, list):
#            self._lines = path_stream_or_string
#        elif isinstance(path_stream_or_string, (io.TextIOWrapper, io.StringIO)):
#            self._lines = lines_from_stream(path_stream_or_string, as_interned)
#        elif isinstance(path_stream_or_string, str):
#            self._lines = lines_from_string(path_stream_or_string, as_interned)
#        else:
#            raise TypeError('Unknown type for arg data: {}'.format(type(path_stream_or_string)))
#        self.name = name
#        self.description = description
#        self.meta = meta
#        self.nprint = 30
#        self.cursor = 0
#
#    def __delitem__(self, line):
#        del self._lines[line]     # "line" is the line number minus one
#
#    def __getitem__(self, key):
#        if isinstance(key, str):
#            return getattr(self, key)
#        return self._lines[key]
#
#    def __setitem__(self, line, value):
#        self._lines[line] = value
#
#    def __iter__(self):
#        for line in self._lines:
#            yield line
#
#    def __len__(self):
#        return len(self._lines)
#
#    def __str__(self):
#        return '\n'.join(self._lines)
#
#    def __contains__(self, item):
#        for obj in self:
#            if item in obj:
#                return True
#
#    def __repr__(self):
#        r = ''
#        nn = len(self)
#        n = len(str(nn))
#        if nn > self.nprint * 2:
#            for i in range(self.nprint):
#                ln = str(i).rjust(n, ' ')
#                r += self._fmt(ln, self._lines[i])
#            r += '...\n'.rjust(n, ' ')
#            for i in range(nn - self.nprint, nn):
#                ln = str(i).rjust(n, ' ')
#                r += self._fmt(ln, self._lines[i])
#        else:
#            for i, line in enumerate(self):
#                ln = str(i).rjust(n, ' ')
#                r += self._fmt(ln, line)
#        return r
#
#
#def lines_from_file(path, as_interned=False, encoding=None):
#    """
#    Create a list of file lines from a given filepath.
#
#    Args:
#        path (str): File path
#        as_interned (bool): List of "interned" strings (default False)
#
#    Returns:
#        strings (list): File line list
#    """
#    lines = None
#    with io.open(path, encoding=encoding) as f:
#        if as_interned:
#            lines = [sys.intern(line) for line in f.read().splitlines()]
#        else:
#            lines = f.read().splitlines()
#    return lines
#
#
#def lines_from_stream(f, as_interned=False):
#    """
#    Create a list of file lines from a given file stream.
#
#    Args:
#        f (:class:`~io.TextIOWrapper): File stream
#        as_interned (bool): List of "interned" strings (default False)
#
#    Returns:
#        strings (list): File line list
#    """
#    if as_interned:
#        return [sys.intern(line) for line in f.read().splitlines()]
#    return f.read().splitlines()
#
#
#def lines_from_string(string, as_interned=False):
#    """
#    Create a list of file lines from a given string.
#
#    Args:
#        string (str): File string
#        as_interned (bool): List of "interned" strings (default False)
#
#    Returns:
#        strings (list): File line list
#    """
#    if as_interned:
#        return [sys.intern(line) for line in string.splitlines()]
#    return string.splitlines()
