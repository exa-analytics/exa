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
from io import StringIO, TextIOWrapper, BufferedReader
from collections import OrderedDict
from exa.typed import Typed, TypedClass
# Python 2 compatibility
if not hasattr(bz2, "open"):
    bz2.open = bz2.BZ2File


def read_file(path, encoding="utf-8"):
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

    def write(self, path, *args, **kwargs):
        """
        Write editor contents to file.

        Args:
            path (str): Full file path
            args: Positional arguments for formatting
            kwargs: Keyword arguments for formatting

        """
        encoding = kwargs.pop("encoding", "utf-8")
        newline = kwargs.pop("newline", "")
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
            found (OrderedDict): Dictionary of results
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

    def find_next(self, *patterns, **kwargs):
        """
        Find the next line with the given text pattern.

        If no match is found, none is returned. If a match is found, the cursor
        position is updated and a tuple of line number and text is returned.

        Args:
            patterns: String pattern(s) to search for
            case (bool): Respect case
            reverse (bool): Search in reverse
            wrap (bool): At end, continue search at beginning (and vice versa)
            cursor (int): Set the line cursor prior to search (optional)

        Returns:
            tup (tuple): Tuple of line number and text for first match
        """
        case = kwargs.pop("case", True)
        reverse = kwargs.pop("reverse", False)
        wrap = kwargs.pop("wrap", False)
        cursor = kwargs.pop("cursor", None)
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
            found = ed.regex("expr")

        Args:
            patterns: Regular expressions
            flags: Python regular expression flags

        Returns:
            found (OrderedDict): Dictionary of results
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
        for i, line in enumerate(self):
            for regex in regexes:
                if regex.search(line):
                    matches[regex.pattern].append((i, line))
        return matches

    def regex_next(self, *patterns, **kwargs):
        """
        Find the next line with a given regular expression pattern.

        If no matches are found, None is returned. Certain flags (such as
        multiline) are not supported by this function.

        Args:
            patterns (regex): Regular expression to search for
            flags (int): Regularexpression compilation flags
            reverse (bool): Search backwards
            wrap (bool): Continue search from beginning/end of file (wraparound end of file)
            cursor (int): Set the cursor prior to searching

        Returns:
            tup (tuple): Tuple of line number and text for first match
        """
        flags = kwargs.pop("flags", 0)
        reverse = kwargs.pop("reverse", False)
        wrap = kwargs.pop("wrap", False)
        cursor = kwargs.pop("cursor", None)
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
            :func:`~exa.core.editor.find_next` and/or
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

    def __init__(self, textobj, encoding="utf-8", nprint=15, ignore=False, **meta):
        """
        Check if accidental filepath but missing file or wrong directory.
        Warn the user unless ignore is true.
        """
        if (isinstance(textobj, six.string_types) and
            os.path.sep in textobj and len(textobj.split("\n")) == 1
            and ignore == False and not os.path.exists(textobj)):
            warnings.warn("Possibly incorrect file path! {}".format(textobj))
        if isinstance(textobj, str) and os.path.exists(textobj):
            meta['filepath'] = textobj
            lines = read_file(textobj, encoding=encoding)
        elif isinstance(textobj, six.string_types):
            lines = str(textobj).splitlines()
        elif isinstance(textobj, (list, tuple)) and isinstance(textobj[0], six.string_types):
            lines = textobj
        elif isinstance(textobj, (TextIOWrapper, StringIO)):
            lines = textobj.read().splitlines()
        elif isinstance(textobj, BufferedReader):
            if textobj.name is not None:
                meta['filepath'] = textobj.name
            lines = textobj.read().decode(encoding).splitlines()
        elif isinstance(textobj, Editor):
            lines = textobj.lines
        else:
            raise TypeError("Object of type {} not supported by Editors.".format(type(textobj)))
        self.lines = lines
        self.cursor = 0
        self.nprint = nprint
        self.meta = meta

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
