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

.. code-block:: python

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
import json
import os, re, sys, bz2, gzip, six
import warnings
import pandas as pd
from abc import abstractmethod
from copy import copy, deepcopy
from collections import Counter
from io import StringIO, TextIOWrapper
from exa.typed import simple_function_factory, yield_typed, create_typed_attr
from .base import ABCBase, ABCBaseMeta


class Editor(six.with_metaclass(ABCBaseMeta, ABCBase)):
    """
    A representation of a file on disk that can be modified programmatically.

    Editor line numbers start at 0. To increase the number of lines
    displayed, increase the value of the ``nprint`` attribute. For large text
    with repeating strings be sure to use the ``as_interned`` argument.
    To change the print format, modify the ``_fmt`` attribute

    Args:
        name (str): Data/file/misc name
        description (str): Data/file/misc description
        meta (dict): Additional meta as key, value pairs
        nrpint (int): Number of lines to display when printing
        cursor (int): Line number position of the cursor
    """
    _getters = ('_get', 'parse')
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
        constants = [match[2:-2] for match in self.regex(csnt, which='text')[csnt]]
        templates = [match[1:-1] for match in self.regex(tmpl, which='text')[tmpl]]
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
        constants = [match[2:-2] for match in self.regex(csnt, which='text')[csnt]]
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
                    if which == "lineno":
                        return i
                    elif which == "text":
                        return str(self[i])
                    else:
                        return (i, str(self[i]))

    def copy(self):
        """Create a copy of the current editor."""
        cls = self.__class__
        lines = self._lines[:]
        as_interned = copy(self.as_interned)
        nprint = copy(self.nprint)
        meta = deepcopy(self.meta)
        encoding = copy(self.encoding)
        return cls(lines, as_interned, nprint, meta, encoding)

    def format(self, *args, **kwargs):
        """
        Populate the editors templates.

        Args:
            \*args: Args for formatting
            \*\*kwargs: Kwargs for formatting
            inplace (bool): If True, overwrite editor's contents (default False)

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
            lineno (int): Line number after which to insert lines
            lines (list, str): List of lines or text to append to the editor

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
            kind (str): One of 'pdcsv', 'pdjson', 'json'
            args: Arguments to be passed to the pandas function
            kwargs: Arguments to be passed to the pandas function

        Note:
            A list of keyword arguments can be found at
            http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
        """
        if kind == 'pdcsv':
            return pd.read_csv(self.to_stream(), *args, **kwargs)
        elif kind == 'pdjson':
            return pd.read_json(self.to_stream(), *args, **kwargs)
        elif kind == 'json':
            return json.load(self.to_stream())
        else:
            raise ValueError("Unexpected argument for kind, {}".format(kind))

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
        kwargs = {'nprint': self.nprint, 'meta': self.meta,
                  'encoding': self.encoding, 'as_interned': self.as_interned}
        return self.__class__(self._lines[key], **kwargs)

    def __setitem__(self, line, value):
        self._lines[line] = value

    def __init__(self, data, as_interned=False, nprint=30, meta=None,
                 encoding='utf-8', ignore_warning=False, **kwargs):
        super(Editor, self).__init__(**kwargs)
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
        self.nprint = nprint
        self.as_interned = as_interned
        self.encoding = encoding
        self.cursor = 0
        if filepath is not None:
            try:
                self.meta['filepath'] = filepath
            except TypeError:
                self.meta = {'filepath': filepath}

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


class SectionsMeta(ABCBaseMeta):
    """
    Metaclass that automatically generates parsing function wrappers.

    Attributes:
        sections (list): A list of tuples of the form [(name, start, end), ...]
    """
    _descriptions = {"sections": "List of sections"}
    sections = list

    def describe(cls):
        """Description of this parser."""
        data = {"Name": cls.name, "Class": cls, "Description": cls.description}
        params = [n.replace("_key_", "") for n in vars(cls) if n.startswith("_key_")]
        if len(params) == 0:
            data["Parameters"] = None
        else:
            data["Parameters"] = params
        return pd.Series(data)

    def __new__(mcs, name, bases, clsdict):
        for attr in yield_typed(mcs):
            f = simple_function_factory("parse", "parse", attr[0])
            clsdict[f.__name__] = f
        clsdict['_descriptions'] = mcs._descriptions
        clsdict['_parsers'] = {}
        clsdict['describe'] = classmethod(mcs.describe)
        return super(SectionsMeta, mcs).__new__(mcs, name, bases, clsdict)


class Sections(six.with_metaclass(SectionsMeta, Editor)):
    """
    A special editor like object tailored to parsing of files that consist of
    multiple, distinct, regions. Regions may, themselves, consist of sections
    or may be directly parsed (see :class:`~exa.core.editor.Section`). The
    following example shows simple use case.

    .. code-block:: python

        import six

        text = '''some
        --------------
        structured
        --------------
        text
        '''

        class SectionsExample(exa.core.editor.Sections):
            name = 'example_sections_parser'
            description = 'Parses files separated by ---'
            _key_sep = '---'                # Arbitrary section separator
            _key_def_sec_name = 'default'   # Default section name

            def _parse(self):
                # The code below depends on the file in question
                delims = self.find(self._key_sep, which='lineno')[self._key_sep]
                starts = [delim + 1 for delim in delims]
                starts.insert(0, 0)
                ends = delims
                ends.append(len(self))
                names = [self._key_def_sec_name]*len(starts)
                self.sections = list(zip(names, starts, ends))

        class ParserMeta(exa.core.editor.SectionsMeta):
            wordcount = int
            wordlist = list
            _descriptions = {'wordcount': "Count of number of words",
                             'wordlist': "List of words"}

        class Parser(six.with_metaclass(ParserMeta, exa.core.editor.Section)):
            description = 'Parser for individual region separated by -* regex'
            name = 'default'

            def _parse(self):
                # Arbitrary what data objects are created here
                self.wordlist = [word for line in self.lines for word in line.split()]
                self.wordcount = len(self.wordlist)


        # The following needs only be performed once,
        # preferably at the module level, hidden from the user.
        SectionsExample.add_section_parsers(Parser)

        # The following shows some useful commands and (commented) print output
        # Prior to using a Sections or Section object one can inspect them
        SectionsExample.describe()
            # Class          <class '__main__.SectionsExample'>
            # Description    Parses files separated by -* regex
            # Name                      example_sections_parser
            # Parameters                    [sep, def_sec_name]
        SectionsExample.describe_parsers()
            # +-------------+------------+------------------+---------------------+
            # | Parser Name | Parameters | Class(es)        | Attributes          |
            # +-------------+------------+------------------+---------------------+
            # | default     | None       | <class 'Parser'> | wordcount, wordlist |
            # +-------------+------------+------------------+---------------------+

        # The object is create just like all editors
        edit = SectionsExample(text)
        edit
            # 0: some
            # 1: --------------
            # 2: structured
            # 3: --------------
            # 4: text
        edit.describe_sections()
            # +------------+-------------+-------+-----+
            # | Section ID | Parser Name | Start | End |
            # +------------+-------------+-------+-----+
            # | 0          | default     | 0     | 1   |
            # +------------+-------------+-------+-----+
            # | 1          | default     | 2     | 3   |
            # +------------+-------------+-------+-----+
            # | 2          | default     | 4     | 5   |
            # +------------+-------------+-------+-----+

    Warning:
        Parsers should be added to sections class objects using the
        :func:`~exa.code.editor.Sections.add_section_parsers` function.
        Parser objects have a ``name`` attribute to identify what section they
        parse.

    Tip:
        Access a parsing parameter using the ``._key_[parameter]`` attribute.
        Access a parsed section using the ``.sectionid`` attribute.
        Access a parser using the ``_parsers[name]`` attribute.

    Note:
        Sections follows the [start, end) convention for line numbering.

    See Also:
        The :class:`~exa.core.editor.Section` objects are section parsers.
        Example usage can be found in :mod:`~exa.core.tests.test_editor`.
    """
    name = None        # Subclasses may set this if needed
    description = None # ditto

    @abstractmethod
    def _parse(self):
        """
        Parsing the the sections attribute occurs here.

        The algorithm is file specific but should conform to creating a ``sections``
        attribute of the following form.

        .. code-block:: python

            [('section name', line_start, line_end), ...]
        """
        pass

    def parse(self):
        """
        Parse the sections of this file and set the ``sections`` attribute.

        See Also:
            :func:`~exa.core.editor.Sections.describe_sections`
        """
        # This helper function is used below; it makes a call self's parse_section
        # function with a given argument.
        def section_parser_helper(i):
            def section_parser():
                self.parse_section(i)
            return section_parser
        # First perform the file specific parse method
        self._parse()
        # Now generate section attributes for the sections present
        self._nsections = len(str(len(self.sections)))
        for i, sec in enumerate(self.sections):
            section = sec[0]
            if section not in self._parsers:
                warnings.warn("No parser for section '{}'!".format(section))
                continue
            secname = "section" + str(i).zfill(self._nsections)
            ptypes = self._parsers[section]
            # Now we perform a bit of class gymnastics:
            # Because we don't want to attach out typed property paradigm
            # (see exa.typed.create_typed_attr) to all instances of this
            # object's class, we dynamically create a copy of this object's
            # class and attach our properties to that class object.
            cls = type(self)
            if not hasattr(cls, '__unique'):
                uniquecls = type(cls.__name__, (cls, ), {})
                uniquecls.__unique = True
                uniquecls.add_section_parsers(*cls._parsers.values())
                self.__class__ = uniquecls
            setattr(self.__class__, secname, create_typed_attr(secname, ptypes))
            # And attach a lazy evaluation method using the above helper
            setattr(self, "parse_" + secname, section_parser_helper(i))

    def parse_all_sections(self):
        """
        Parse data (or sub-sections) of each section identified by this object.

        For each section parsed, a corresponding attributed name ``sectionID``
        is created; nothing is returned by this function and no arguments are
        accepted.

        See Also:
            Two very useful functions, :func:`~exa.core.editor.Sections.describe_sections`
            and :func:`~exa.editor.Sections.describe_parsers` show section names
            and numbers, and section parsers, respectively.
        """
        for i in range(self._nsections):
            self.parse_section(i)

    def parse_section(self, number):
        """
        Parse specific section of this object.

        Parse section data can be accessed via the ``sectionID`` attribute, where
        ID is the number of the section as listed in the ``describe_sections``
        table or in the order given by the ``sections`` attribute.

        Args:
            number (int): Section number (of the ``sections`` list)

        See Also:
            Two very useful functions, :func:`~exa.core.editor.Sections.describe_sections`
            and :func:`~exa.editor.Sections.describe_parsers` show section names
            and numbers, and section parsers, respectively.
        """
        section, start, end = self.sections[number]
        if section not in self._parsers:
            warnings.warn("No parser for section '{}'!".format(section))
            return
        secname = "section" + str(number).zfill(self._nsections)
        # Note that we don't actually parse anything until a value is in fact
        # request, e.g. sections.parser.dataobj
        setattr(self, secname, self._parsers[section](self[start:end]))

    def delimiters(self):
        """Describes the patterns used to disambiguate regions of the file."""
        return [(name, getattr(self, name)) for name in vars(self) if name.startswith("_key_")]

    def describe_sections(self):
        """
        Display available section names and numbers.

        Note:
            This method only has meaning once sections have been parsed.
        """
        sections = self.sections
        if len(sections) == 0:
            warnings.warn("No sections identified.")
        else:
            df = pd.DataFrame(sections, columns=["Parser Name", "Start", "End"])
            df.index.name = "Section ID"
            return df

    @classmethod
    def describe_parsers(cls):
        """Display available section parsers."""
        data = {}
        for key, item in cls._parsers.items():
            params = [n.replace("_key_", "") for n in vars(item) if n.startswith("_key_")]
            params = None if params == [] else ", ".join(params)
            attrs = [attr[0] for attr in yield_typed(item)]
            attrs = None if attrs == [] else ", ".join(attrs)
            data[key] = (params, item, attrs)
        if len(data) == 0:
            warnings.warn("No parsers added.")
        else:
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index.name = "Parser Name"
            df.columns = ["Parameters", "Class(es)", "Attributes"]
            return df

    @classmethod
    def add_section_parsers(cls, *args, **kwargs):
        """
        Add section parsers classes.

        .. code-block:

            Sections.add_section_parsers(Section1, Section2, ...)
        """
        cls._parsers.update({str(s.name): s for s in args})


class Section(six.with_metaclass(SectionsMeta, Editor)):
    """
    An editor like object that corresponds to a specific and distinct region of
    a file and contains parsing functionality tailored to this region. The
    :class:`~exa.core.editor.Section` object can be used standalone or in concert
    with the :class:`~exa.core.editor.Sections` object for parsing of complex
    files with multiple regions.

    See Also:
        :class:`exa.core.editor.Sections`

    Warning:
        Subclasses must set the class attribute 'name' as the parser name.
    """
    name = None        # Set by subclass
    description = None # ditto

    @abstractmethod
    def _parse(self):
        """
        The parsing algorithm, specific to this section, belongs here.

        This function should set all data object attributes as defined by in
        the corresponding metaclass (e.g. :class:`~exa.core.editor.SectionsMeta`).

        See Also:
            An example implementation can be found in the docs of
            :class:`~exa.core.editor.Sections`.
        """
        pass

    def parse(self):
        """Parse all data objects."""
        self._parse()

    @classmethod
    def describe_attributes(cls):
        """Description of data attributes associated with this parser."""
        df = {}
        for name, types in yield_typed(cls):
            df[name] = (cls._descriptions[name], types)
        df = pd.DataFrame.from_dict(df, orient='index')
        df.columns = ["Description", "Type"]
        df.index.name = "Attribute"
        return df


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
