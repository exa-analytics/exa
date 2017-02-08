# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Editor
####################################
The :class:`~exa.core.editor.Editor` class is a way for programmatic text-
editor-like manipulation of files on disk. The goal of an editor is to facilitate
easy conversion or extraction of data from a text file. It does not strive to be
a full featured text editor. A large number of Pythonic operations can be performed
on editors:

.. code-block:: Python

    editor = Editor(file.txt)       # Create an editor from a file
    editor = Editor(file.txt.gz)    # Automatically decompresses files
    editor = Editor(file.txt.bz2)
    for line in editor:             # Iterate over lines in the file
        pass
    if 'text' in editor:            # True if "text" appears on any line
        True

Text lines are stored in memory; file handles are only open during reading and
writing. For large repetitive files, memoization can reduce the memory footprint
(see the **as_interned** kwarg).

See Also:
    Common examples of data objects are  :class:`~exa.core.dataseries.DataSeries`
    and :class:`~exa.core.dataframe.DataFrame` among others.
"""
import os, re, sys, bz2, gzip, six
import pandas as pd
from abc import abstractmethod
from copy import copy, deepcopy
from collections import Counter
from io import StringIO, TextIOWrapper
from exa.typed import Meta, simple_function_factory, yield_typed


class Editor(object):
    """
    A representation of a file on disk that can be modified programmatically.

    Editor line numbers start at 0. To increase the number of lines
    displayed, increase the value of the ``nprint`` attribute. For large text
    with repeating strings be sure to use the ``as_interned`` argument.
    To change the print format, modify the ``_fmt`` attribute

    Args:
        name (str): Data/file/misc name
        description (str): Data/file/misc description
        meta (dict): Additional metadata as key, value pairs
        nrpint (int): Number of lines to display when printing
        cursor (int): Line number position of the cursor
    """
    _fmt = '{0}: {1}\n'.format   # Format for printing lines (see __repr__)

    @property
    def templates(self):
        """
        Display a list of templates.

        .. code-block:: text

            tmpl = "this is a {template}"
            tmpl.format(template="other text")    # prints "this is a other text"

        See Also:
            Python string formatting is very powerful. See the `docs`_ for more
            information and usage examples.

        .. _docs: https://docs.python.org/3.6/library/string.html
        """
        csnt = r"{{[\w\d]*}}"
        tmpl = r"{[\w\d]*}"
        constants = [match[2:-2] for match in self.regex(csnt, which='values')[csnt]]
        templates = [match[1:-1] for match in self.regex(tmpl, which='values')[tmpl]]
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
        csnt = r"{{[\w\d]*}}"
        constants = [match[2:-2] for match in self.regex(csnt, which='values')[csnt]]
        return sorted(constants)

    def regex(self, *patterns, **kwargs):
        """
        Match a line or lines by the specified regular expression(s).

        Args:
            \*patterns: Regular expressions
            which: If none, returns (lineno, text), else "lineno" or "text"
            flags: Python regex flags (default re.MULTILINE)

        Returns:
            results (dict): Dictionary with pattern keys and list of values

        See Also:
            https://en.wikipedia.org/wiki/Regular_expression
        """
        which = kwargs.pop('which', None)
        flags = kwargs.pop('flags', re.MULTILINE)
        results = {}
        self_str = str(self)
        for pattern in patterns:
            match = pattern
            pattern_results = []
            if not type(pattern).__name__ == "SRE_Pattern":
                match = re.compile(pattern, flags)
            if which == "lineno":
                for m in match.finditer(self_str):
                    pattern_results.append(self_str.count("\n", 0, m.start()) + 1)
            elif which == "text":
                for m in match.finditer(self_str):
                    pattern_results.append(m.group())
            else:
                for m in match.finditer(self_str):
                    pattern_results.append((self_str.count("\n", 0, m.start()) + 1, m.group()))
            results[match.pattern] = pattern_results
        return results

    def find(self, *patterns, **kwargs):
        """
        Search for patterns line by line.

        Args:
            \*strings (str): Any number of strings to search for
            which: If None, returns (lineno, text), else "lineno" or "text"

        Returns:
            results (dict): Dictionary with pattern keys and list of (lineno, line) values
        """
        which = kwargs.pop('which', None)
        results = {pattern: [] for pattern in patterns}   # Iterate twice over
        for i, line in enumerate(self):                   # patterns because we
            for pattern in patterns:                      # search line by line
                if pattern in line:
                    if which == "lineno":
                        results[pattern].append(i)
                    elif which == "text":
                        results[pattern].append(line)
                    else:
                        results[pattern].append((i, line))
        return results

    def find_next(self, pattern, which=None, reverse=False):
        """
        From the current cursor position, find the next occurrence of the pattern.

        Args:
            pattern (str): String to search for from the cursor
            which: If None, returns (lineno, text), else "lineno" or "text"
            reverse (bool): Find next in reverse

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
                    if which == "keys":
                        return i
                    elif which == "values":
                        return str(self[i])
                    else:
                        return (i, str(self[i]))

    def copy(self):
        """Create a copy of the current editor."""
        cls = self.__class__
        lines = self._lines[:]
        as_interned = copy(self.as_interned)
        name = copy(self.name)
        nprint = copy(self.nprint)
        metadata = deepcopy(self.metadata)
        enc = copy(self.encoding)
        return cls(lines, as_interned, nprint, name, metadata, enc)

    def format(self, *args, **kwargs):
        """
        Populate the editors templates.

        Args:
            \*args: Args for formatting
            \*\*kwargs: Kwargs for formatting
            inplace (bool): If True, overwrite editor's contents with formatted contents (default False)

        Returns:
            formatted: Returns the formatted editor (if inplace is False)
        """
        inplace = kwargs.pop('inplace', False)
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
            *args: Positional arguments for formatting
            **kwargs: Keyword arguments for formatting
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
            lines (list, str): List of lines or str text to append to the editor

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
            lines (list, str): List of lines or str text to append to the editor

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
            lineno (int): Line number after which to insert lines
            lines (list, str): List of lines or str text to append to the editor

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
        for i, line in enumerate(self):
            while pattern in line:
                line = line.replace(pattern, replacement)
            lines.append(line)
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

    def to_stringio(self):
        """Send to StringIO object."""
        return StringIO(str(self))

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
        del self._lines[line]     # "line" is the line number minus one

    def __getitem__(self, key):
        if isinstance(key, six.string_types):
            return getattr(self, key)
        kwargs = {'nprint': self.nprint, 'description': self.description,
                  'name': self.name, 'meta': self.meta, 'encoding': self.encoding,
                  'as_interned': self.as_interned}
        return self.__class__(self._lines[key], **kwargs)

    def __setitem__(self, line, value):
        self._lines[line] = value

    def __init__(self, data, as_interned=False, nprint=30, description=None,
                 name=None, meta=None, encoding='utf-8', ignore_warning=False):
        filepath = None
        if check_path(data, ignore_warning):
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
            raise TypeError('Unknown type for arg data: {}'.format(type(data)))
        self.name = name
        self.description = description
        self.meta = meta
        self.nprint = 30
        self.as_interned = as_interned
        self.encoding = encoding
        self.cursor = 0
        if self.meta is None and filepath is not None:
            self.meta = {'filepath': filepath}
        elif filepath is not None and 'filepath' not in self.meta:
            self.meta['filepath'] = filepath

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


class SectionsMeta(Meta):
    """
    Metaclass that automatically generates functions.
    """
    _getters = ("parse", )
    _attr_descriptions = {"sections": "List of sections"}
    sections = list

    def __new__(mcs, name, bases, clsdict):
        for attr_name, definition in yield_typed(mcs):
            f = simple_function_factory("parse", "parse", attr_name)
            clsdict[f.__name__] = f
        clsdict["_attr_descriptions"] = mcs._attr_descriptions
        return super(SectionsMeta, mcs).__new__(mcs, name, bases, clsdict)


class Sections(six.with_metaclass(SectionsMeta, Editor)):
    """
    A special editor like object tailored to parsing of files that consist of
    multiple, distinct, regions. Each region corresponds to a
    :class:`~exa.core.editor.Section` object that contains the appropriate
    parsing functionality specific to (only) that region. Complex files' regions
    may themselves be :class:`~exa.core.editor.Sections` objects.

    Note:
        Use the 'describe' property to see what data objects are available.

    See Also:
        :class:`~exa.core.editor.Section`
    """
    name = None
    parsers = {}

    def delimiters(self):
        """Describe the patterns used to disambiguate regions of the file."""
        return [(name, getattr(self, name)) for name in vars(self) if name.startswith("_key_")]

    def describe(self):
        """Describe section parsers and/or (sub)sections are handled by this object."""
        return self.parsers

    def get_section_bounds(self, section):
        """
        Get the start and end point of a given section.

        Args:
            section (str or int): Section name or integer index

        Returns:
            tup (tuple): Tuple of form (start, end, name, number)
        """
        end = float('inf')    # So that abs(...) < abs(...) works (see below)
        if isinstance(section, int):
            name = list(self.sections.keys())[section]
            number = section
        else:
            name = section
            number = list(self.sections.keys()).index(section)
        start = self.sections[name]
        for key, lineno in self.sections:
            if lineno > start and abs(lineno - start) < abs(end - start):
                end = lineno
        return (start, end, name, number)

    def get_section(self, section):
        """
        Get the Section editor associated with the named or integer section.

        Args:
            section (str or int): Section name or integer index

        Returns:
            section (Section): Section editor object specific to the given section
        """
        start, end, name, number = self.get_section_bounds(section)
        return self._parsers[name](str(self[start:end]))

    @abstractmethod
    def parse(self):
        """Section identification algorithm belongs here."""
        pass

    @classmethod
    def add_section_parsers(cls, *args):
        """
        Add section parsers to the editor class.

        .. code-block:

            Sections.add_section_parsers(Section1, Section2, ...)
        """
        cls.parsers.update({s.name: s for s in args})



class SectionMeta(SectionsMeta):
    """Metaclass for :class:`~exa.core.editor.Section` objects."""
    _getters = ("parse", )
    _attr_descriptions = None


class Section(six.with_metaclass(SectionMeta, Editor)):
    """
    An editor like object that corresponds to a specific and distinct region of
    a file and contains parsing functionality tailored to this region. The
    :class:`~exa.core.editor.Section` object can be used standalone or in concert
    with the :class:`~exa.core.editor.Sections` object for parsing of complex
    files with multiple regions.

    .. code-block: Python

    See Also:
        :class:`exa.core.editor.Sections`
    """
    name = None

    def describe(self):
        """Description of data attributes associated with this parser."""
        description = {}
        for name, attr in self._yield_typed():
#        for name, attr in vars(self.__class__).items():
#            if isinstance(attr, property):
            description[name] = (self._attr_descriptions[name], attr)
        descr = pd.DataFrame.from_dict(description, orient='index')
        descr.columns = ["description", "type"]
        descr.index.name = "attribute"
        return descr

    @abstractmethod
    def parse(self):
        """The parsing algorithm, specific to this section, belongs here."""
        pass


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
        if (ignore_warning or os.path.exists(path) or
            (len(path.split("\n")) == 1 and ("\\" in path or "/" in path))):
            return True
    except TypeError:
        pass
    return False


def read_file(path, as_interned=False, encoding='utf-8'):
    """
    Create a list of file lines from a given filepath.

    Args:
        path (str): File path
        as_interned (bool): List of "interned" strings (default False)

    Returns:
        strings (list): File line list
    """
    lines = None
    if path.endswith(".gz"):
        f = gzip.open(path, 'rb')
    elif path.endswith(".bz2"):
        f = bz2.open(path, 'rb')
    else:
        f = open(path, 'rb')
    read = f.read()
    try:
        read = read.decode(encoding)    # For .gz and .bz2 files
    except AttributeError:
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
        as_interned (bool): List of "interned" strings (default False)

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
        as_interned (bool): List of "interned" strings (default False)

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
        \*editors: Collection of editors (in order) to be concatenated
        \*\*kwargs: Arguments for editor creation

    Returns:
        editor: An instance of an editor
    """
    classes = [ed.__class__ for ed in editors]
    cls = Counter(classes).most_common(1)[0][0]
    lines = []
    for ed in editors:
        lines += ed._lines
    return cls(lines, **kwargs)
