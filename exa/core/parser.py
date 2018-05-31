# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Parsing Editors
####################################
This module provides editors tailored to parsing small/medium sized text files
that do not have a consistent structure. The primary goal of parsers is to
facilitate the creation of modular parsing units. Each parsing unit is
responsible for transforming a small section of text into an appropriate Python
data object. Parsing units can be connected under a single API call for ease,
but each unit should only ever be responsible for a parsing a single, typically
repetitive, section of text.

.. code-block:: python

    text = '''datablock
    ...

    otherblock
    this section has metadata or text while the other might have numbers

    datablock
    ...

    otherblock
    blah
    '''

    class DBlock(Parser):
        _start = "datablock"    # Start line is the string datablock
        _end = None             # Custom ending line
        data = Typed(DataFrame) # Example data object parsed by this section specific parser

        def _parse_end(self, starts):
            # For each starting point find the next blank line
            # this is specific to this particular file
            pass

        def _parse_data(self):
            # Parsing logic for constructing the data object
            pass

    class OBlock(Parser):
        _start = re.compile("otherblock")    # To use regex searching, set compiled regex
        _end = None                          # Again custom end line searching

        def _parse_end(self, starts):
            pass

    class Wrapper(Parser):
        # Could be used to parse additional headers or footers in the file
        pass

    Wrapper.add_parsers(DBlock, OBlock)

    parser = Wrapper(text)
    parser.sections           # Automatically display 4 total sections, 2 datablocks, 2 otherblocks
    parser.get_section(0)     # The sections object is sorted by starting line number so this is the first datablock
    parser.info()             # Display information about available data objects/additional parsers
    parser.parse()            # Populate all data objects on each of parsers (per section)

See Also:
    For additional information about searching, see
    :class:`~exa.core.editor.Editor` and :class:`~exa.core.editor.Match`,
    :class:`~exa.core.editor.Matches`, and :class:`~exa.core.editor.Found`.
"""
#import six
#from .editor import Editor
#from .data import DataFrame, Column, Index
#from exa.typed import Typed, yield_typed
#
#
#class SectionsParsingFailure(Exception):
#    """Exception raised when sections of a parser cannot be identified."""
#    def __init__(self, parser, startlines, endlines):
#        m = len(startlines)
#        n = len(endlines)
#        msg = "Found {} starting and {} ending lines for parser {}".format(m, n, parser)
#        super(SectionsParsingFailure, self).__init__(msg)
#
#
#class ParsingError(Exception):
#    """Raised when parsing failure (on sections or otherwise) occurs."""
#    def __init__(self, parser, info):
#        msg = "Parsing failure for parser {} when searching {}".format(parser, info)
#        super(ParsingError, self).__init__(msg)
#
#
#class Sections(DataFrame):
#    """
#    A schematic representation of a file parser that shows available sections
#    to be parsed.
#
#    This dataframe does not perform any parsing itself. It provides a summary
#    view of the available parsers, each with their own data objects, that can
#    be parsed. Each section dataframe is specific to the parser/editor on
#    which it is an attribute. Although verbose, fully qualified class names,
#    for parsers, are used to remove ambiguity in the case parsing classes have
#    identical names.
#
#    +---------+----------------+------------+----------+
#    | section | parser (class) | start line | end line |
#    +=========+================+============+==========+
#    | 0       | Editor         |  0         | 10       |
#    +---------+----------------+------------+----------+
#    | etc.    | misc           |  etc.      | etc.     |
#    +---------+----------------+------------+----------+
#    """
#    section = Index(int)
#    startline = Column(int)
#    endline = Column(int)
#    parser = Column(str)
#
#    @classmethod
#    def from_lists(cls, startlines, endlines, parsers):
#        """
#        Create a dataframe corresponding to sections of an editor.
#
#        Args:
#            startlines (array): Array of starting line numbers
#            endlines (array): Array of stopping line numbers
#            parsers (array): Array of parser classes for specific sections
#            ed (Editor): Editor to which the sections belong
#        """
#        df = DataFrame.from_dict({'startline': startlines,
#                                  'endline': endlines,
#                                  'parser': parsers})
#        df = df[["startline", "endline", "parser"]]
#        return cls(df)
#
#    def __init__(self, *args, **kwargs):
#        super(Sections, self).__init__(*args, **kwargs)
#        self.sort_values('startline', inplace=True)
#        self.reset_index(drop=True, inplace=True)
#
#
#class Parser(Editor):
#    """
#    An Editor-like object built for parsing small/medium files that are
#    semi-structured.
#
#    Parsers are written for a specific block of text that corresponds to one or
#    more data objects. The are atomistic and expect no outside information to
#    perform their parsing function. For parsing functions that cannot fit into
#    this paradigm, 'wrapping' parser classes can be written which handle the
#    special cases.
#
#    .. code-block:: python
#
#        class BlockParser(Parser):
#            _start = regex_or_string    # Identifier that denotes start of block
#            _end = regex_or_string      # Identifier that denotes end of block
#
#            def _parse(self):
#                pass                    # Function that transforms block text to python object
#
#        class Wrapper(Parser):
#            def _parse(self):
#                pass                    # Function that handles 'special' parsing (see above)
#
#        Wrapper.add_parsers(BlockParser)
#    """
#    _setters = ("parse", "_parse")
#    _start = None
#    _end = None
#    _f = ("_parsers", )    # Forbidden names
#    sections = Typed(Sections, doc="Schematic representation of text/file.")
#
#    def info(self):
#        """
#        Display information about data objects and attached parsers.
#        """
#        basenames = list(yield_typed(Parser))
#        names = []
#        classes = []
#        descriptions = []
#        for parser in self._parsers:
#            if hasattr(parser, "__module__"):
#                nam = ".".join((parser.__module__, parser.__name__))
#            else:
#                nam = parser.__name__
#            current = list(yield_typed(parser))
#            ns = list(set(current).difference(basenames))
#            ds = [getattr(parser, n).__doc__.replace("\n\n__typed__", "") for n in ns]
#            cs = [nam]*len(ns)
#            names += ns
#            classes += cs
#            descriptions += ds
#        df = DataFrame.from_dict({'name': names, 'class': classes,
#                                  'description': descriptions})
#        df = df[["name", "class", "description"]].sort_values("name").reset_index(drop=True)
#        return df
#
#    def parse(self):
#        """
#        Recursively parse all data objects from the file's sections/parsers/text.
#
#        See Also:
#            :func:`~exa.core.parser.Parser.info`
#        """
#        def check(n):
#            if any(n.startswith(s) for s in self._setters) and n not in self._f:
#                return True
#            return False
#        # First parse the sections
#        if not hasattr(self, "_sections"):
#            self.parse_sections()
#        # Second parse the data objects (if applicable)
#        base = [n for n in dir(Parser) if check(n)]
#        live = [n for n in dir(self) if check(n)]
#        names = set(live).difference(base)
#        for name in names:
#            getattr(self, name)()
#        # Last perform any auxiliary parsing
#        if hasattr(self, "_parse"):
#            self._parse()
#
#    def parse_sections(self):
#        """
#        Identify sections of the current editor's text/file text.
#
#        For all 'added parsers' (see :func:`~exa.core.parser.Parser.add_parsers`)
#        currently attached to this class object, search to text contents of the
#        current object's instance and identify all sections, sub-sections, etc.
#        """
#        def selector(parser):
#            # Helper function that adds all search strings to our lists
#            # so that we iterate over the file as few times as possible.
#            # Note that the Editor's .find and .regex methods deduplicate
#            # patterns passed.
#            for attrname in ("_start", "_end"):
#                attr = getattr(parser, attrname)
#                if type(attr).__name__ == "SRE_Pattern":
#                    regex.append(attr)
#                elif isinstance(attr, str):
#                    find.append(attr)
#
#        # Bin all of search strings/regex
#        regex = []    # for .regex()
#        find = []     # for .find
#        for parser in self._parsers:
#            selector(parser)
#        # Perform file searching
#        rfound = self.regex(*regex)
#        ffound = self.find(*find)
#        # Now construct the sections dataframe by selecting, for each
#        # parser (including self) the start/end string/regex and
#        # adding it to the sections dataframe.
#        starts = []
#        ends = []
#        parsers = []
#        for parser in self._parsers:
#            delayed = 0
#            # Start lines
#            if parser._start is None:
#                delayed = 1
#            elif isinstance(parser._start, six.string_types):
#                start = ffound[parser._start]
#            else:
#                start = rfound[parser._start.pattern]
#            # End lines
#            if parser._end is None:
#                delayed = 2 if delayed == 0 else 3
#            elif isinstance(parser._end, six.string_types):
#                end = ffound[parser._end]
#            else:
#                end = rfound[parser._end.pattern]
#            # Special or both
#            if delayed == 1:    # _parse_start custom starting points
#                start = self._parse_1(parser, end)
#            elif delayed == 2:  # _parse_end custom ending points
#                end = self._parse_2(parser, start)
#            elif delayed == 3:
#                try:
#                    start, end = self._parse_3(parser)
#                except NotImplementedError:
#                    start, end = [], []
#            # Sanity check
#            if len(start) != len(end):
#                raise SectionsParsingFailure(parser, start, end)
#            elif any(s is None for s in start):
#                raise ParsingError(parser, "start lines.")
#            elif any(e is None for e in end):
#                raise ParsingError(parser, "end lines.")
#            starts += [s[0] for s in start]
#            ends += [e[0]+1 for e in end]
#            parsers += [parser]*len(start)
#        self.sections = Sections.from_lists(starts, ends, parsers)
#
#    def get_section(self, key):
#        """
#        Generate an editor corresponding to an identified section.
#
#        Args:
#            key (int): Integer corresponding to section
#
#        Returns:
#            ed (Editor): A correct editor/parser corresponding to the section
#        """
#        if key not in self.sections.index:
#            key = self.sections.index[key]
#        start, stop, cls = self.sections.loc[key, ["startline", "endline", "parser"]]
#        return cls(self.lines[start:stop])
#
#    def get_sections(self, cls):
#        """
#        Iterate (sequentially) overall sections with a given class type
#        (or name - if names are unique).
#
#        Args:
#            cls: String class name or class object
#
#        Returns:
#            iterator: Iterator over each section that matches the criteria
#        """
#        if isinstance(cls, six.string_types):
#            self.sections['name'] = self.sections['parser'].apply(lambda cls: cls.__name__)
#            if len(self.sections.loc[self.sections['name'] == cls, 'parser'].unique()) != 1:
#                raise NameError("Duplicate parser names, ambiguous parser requested.")
#            cls = self.sections.loc[self.sections['name'] == cls, 'parser'].values[0]
#            del self.sections['name']
#        for key in self.sections[self.sections['parser'] == cls].index.values:
#            yield self.get_section(key)
#
#    def _parse_1(self, parser, stops):
#        """
#        Wrapper for calling custom start parsing. The function
#        :func:`~exa.core.parser.Parser._parse_start` is called.
#        """
#        return parser(self)._parse_start(stops)    # Does not copy lines
#
#    def _parse_2(self, parser, starts):
#        """
#        Wrapper for calling custom end parsing. The function
#        :func:`~exa.core.parser.Parser._parse_end` is called.
#        """
#        return parser(self)._parse_end(starts)     # Do not copy lines
#
#    def _parse_3(self, parser):
#        """
#        Wrapper for calling custom start and end parsing. The function
#        :func:`~exa.core.parser.Parser._parse_both` is called.
#        """
#        return parser(self)._parse_both()          # Ditto
#
#    def _parse_start(self, stops):
#        """
#        Custom start parsing if needed (i.e. to be overwritten).
#
#        Should return a list of 2-tuples of line number, line text pairs.
#
#        .. code-block:: python
#
#            [(i, self.lines[i]), (j, self.lines[j]), ...]
#        """
#        raise NotImplementedError("No implementation of _parse_start for {}".format(self.__class__))
#
#    def _parse_end(self, starts):
#        """
#        Custom end parsing, if needed.
#
#        Should return a list of 2-tuples of line number, line text pairs.
#
#        .. code-block:: python
#
#            [(i, self.lines[i]), (j, self.lines[j]), ...]
#        """
#        raise NotImplementedError("No implementation of _parse_end for {}".format(self.__class__))
#
#    def _parse_both(self):
#        """
#        Custom start and end parsing, if needed.
#
#        Should return two lists. Each list is a list of 2-tuples of line number,
#        line text pairs. The first list is interpreted as start and the second
#        as end points.
#
#        .. code-block:: python
#
#            ([(i, self.lines[i]), (j, self.lines[j]), ...],
#             [(i, self.lines[i]), (j, self.lines[j]), ...])
#        """
#        raise NotImplementedError("No implementation of _parse_both for {}".format(self.__class__))
#
#    @classmethod
#    def add_parsers(cls, *parsers):
#        """
#        Add additional (section) parsers to the current parsing system.
#
#        .. code-block:: python
#
#            class P0(Parser):
#                pass
#
#            class P1(Parser):
#                pass
#
#            class Wrapper(Parser):
#                pass
#
#            Wrapper.add_parsers(P0, P1)    # Needs to be performed only once
#            parser = Wrapper(myfile)
#        """
#        # A bit of deduplication is necessary
#        def get(*parsers):
#            dct = {}
#            for p in parsers:
#                if hasattr(p, "__module__"):
#                    n = ".".join((p.__module__, p.__name__))
#                else:
#                    n = p.__name__
#                dct[n] = p
#            return dct
#
#        if not hasattr(cls, "_parsers"):
#            setattr(cls, "_parsers", [])
#        current = get(*cls._parsers)
#        new = get(*parsers)
#        current.update(new)
#        cls._parsers = list(current.values())
#
#    def __init__(self, *args, **kwargs):
#        super(Parser, self).__init__(*args, **kwargs)
#        self.add_parsers(self.__class__)
