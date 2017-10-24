# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
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
import six
from .editor import Editor
from .data import DataFrame, Column, Index
from exa.typed import Typed, yield_typed


class SectionsParsingFailure(Exception):
    """Exception raised when sections of a parser cannot be identified."""
    def __init__(self, parser, startlines, endlines):
        m = len(startlines)
        n = len(endlines)
        msg = "Found {}, {} start, end lines for parser {}".format(m, n, parser)
        super(SectionsParsingFailure, self).__init__(msg)


class Sections(DataFrame):
    """
    A schematic representation of a file parser that shows available sections
    to be parsed.

    This dataframe does not perform any parsing itself. It provides a summary
    view of the available parsers, each with their own data objects, that can
    be parsed. Each section dataframe is specific to the parser/editor on
    which it is an attribute. Although verbose, fully qualified class names,
    for parsers, are used to remove ambiguity in the case parsing classes have
    identical names.

    +---------+----------------+------------+----------+
    | section | parser (class) | start line | end line |
    +=========+================+============+==========+
    | 0       | Editor         |  0         | 10       |
    +---------+----------------+------------+----------+
    | etc.    | misc           |  etc.      | etc.     |
    +---------+----------------+------------+----------+
    """
    section = Index(int)
    startline = Column(int)
    endline = Column(int)
    parser = Column(str)

    @classmethod
    def from_lists(cls, startlines, endlines, parsers):
        """
        Create a dataframe corresponding to sections of an editor.

        Args:
            startlines (array): Array of starting line numbers
            endlines (array): Array of stopping line numbers
            parsers (array): Array of parser classes for specific sections
            ed (Editor): Editor to which the sections belong
        """
        df = DataFrame.from_dict({'startline': startlines,
                                  'endline': endlines,
                                  'parser': parsers})
        df = df[["startline", "endline", "parser"]]
        return cls(df)

    def __init__(self, *args, **kwargs):
        super(Sections, self).__init__(*args, **kwargs)
        self.sort_values('startline', inplace=True)
        self.reset_index(drop=True, inplace=True)


class Parser(Editor):
    """
    An Editor-like object built for parsing small/medium files that are
    semi-structured.

    Parsers are written for a specific block of text that corresponds to one or
    more data objects. The are atomistic and expect no outside information to
    perform their parsing function. For parsing functions that cannot fit into
    this paradigm, 'wrapping' parser classes can be written which handle the
    special cases.

    .. code-block:: python

        class BlockParser(Parser):
            _start = regex_or_string    # Identifier that denotes start of block
            _end = regex_or_string      # Identifier that denotes end of block

            def _parse(self):
                pass                    # Function that transforms block text to python object

        class Wrapper(Parser):
            def _parse(self):
                pass                    # Function that handles 'special' parsing (see above)

        Wrapper.add_parsers(BlockParser)
    """
    _setters = ("parse", "_parse")
    _start = None
    _end = None
    sections = Typed(Sections, doc="Schematic representation of text/file.")

    def info(self):
        """
        Display information about data objects and attached parsers.
        """
        basenames = list(yield_typed(Parser))
        names = []
        classes = []
        descriptions = []
        for parser in self._parsers:
            if hasattr(parser, "__module__"):
                nam = ".".join((parser.__module__, parser.__name__))
            else:
                nam = parser.__name__
            current = list(yield_typed(parser))
            ns = list(set(current).difference(basenames))
            ds = [getattr(parser, n).__doc__.replace("\n\n__typed__", "") for n in ns]
            cs = [nam]*len(ns)
            names += ns
            classes += cs
            descriptions += ds
        df = DataFrame.from_dict({'name': names, 'class': classes,
                                  'description': descriptions})
        df = df[["name", "class", "description"]].sort_values("name").reset_index(drop=True)
        return df

    def parse(self):
        """
        Recursively parse all data objects from the file's sections/parsers/text.

        See Also:
            :func:`~exa.core.parser.Parser.info`
        """
        # First parse the sections
        if not hasattr(self, "_sections"):
            self.parse_sections()
        # Second parse the data objects (if applicable)
        check = lambda n: any(n.startswith(setter) for setter in self._setters)
        base = [n for n in dir(Parser) if check(n)]
        live = [n for n in dir(self) if check(n)]
        names = set(live).difference(base)
        for name in names:
            getattr(self, name)()
        # Last perform any auxiliary parsing
        if hasattr(self, "_parse"):
            self._parse()

    def parse_sections(self):
        """
        Identify sections of the current editor's text/file text.

        For all 'added parsers' (see :func:`~exa.core.parser.Parser.add_parsers`)
        currently attached to this class object, search to text contents of the
        current object's instance and identify all sections, sub-sections, etc.
        """
        def selector(parser):
            # Helper function that adds all search strings to our lists
            # so that we iterate over the file as few times as possible.
            # Note that the Editor's .find and .regex methods deduplicate
            # patterns passed.
            for attrname in ("_start", "_end"):
                attr = getattr(parser, attrname)
                if type(attr).__name__ == "SRE_Pattern":
                    regex.append(attr)
                elif isinstance(attr, str):
                    find.append(attr)

        # Bin all of search strings/regex
        regex = []    # for .regex()
        find = []     # for .find
        for parser in self._parsers:
            selector(parser)
        # Perform file searching
        rfound = self.regex(*regex)
        ffound = self.find(*find)
        # Now construct the sections dataframe by selecting, for each
        # parser (including self) the start/end string/regex and
        # adding it to the sections dataframe.
        starts = []
        ends = []
        parsers = []
        for parser in self._parsers:
            delayed = 0
            # Start lines
            if parser._start is None:
                delayed = 1
            elif isinstance(parser._start, six.string_types):
                start = ffound[parser._start]
            else:
                start = rfound[parser._start.pattern]
            # End lines
            if parser._end is None:
                delayed = 2 if delayed == 0 else 3
            elif isinstance(parser._end, six.string_types):
                end = ffound[parser._end]
            else:
                end = rfound[parser._end.pattern]
            # Special or both
            if delayed == 1:    # _parse_start custom starting points
                start = self._parse_1(parser, end)
            elif delayed == 2:  # _parse_end custom ending points
                end = self._parse_2(parser, start)
            elif delayed == 3:
                try:
                    start, end = self._parse_3(parser)
                except NotImplementedError:
                    start, end = [], []
            # Sanity check
            if len(start) != len(end):
                raise SectionsParsingFailure(parser, starts, ends)
            starts += [s[0] for s in start]
            ends += [e[0]+1 for e in end]
            parsers += [parser]*len(start)
        self.sections = Sections.from_lists(starts, ends, parsers)

    def get_section(self, key):
        """
        Generate an editor corresponding to an identified section.

        Args:
            key (int): Integer corresponding to section

        Returns:
            ed (Editor): A correct editor/parser corresponding to the section
        """
        if key not in self.sections.index:
            key = self.sections.index[key]
        start, stop, cls = self.sections.loc[key, ["startline", "endline", "parser"]]
        return cls(self.lines[start:stop])

    def get_sections(self, cls):
        """
        Iterate (sequentially) overall sections with a given class type
        (or name - if names are unique).

        Args:
            cls: String class name or class object

        Returns:
            iterator: Iterator over each section that matches the criteria
        """
        if isinstance(cls, six.string_types):
            self.sections['name'] = self.sections['parser'].apply(lambda cls: cls.__name__)
            if self.sections.drop_duplicates("name").shape != self.sections.shape:
                raise NameError("Duplicate parser names, ambiguous parser requested.")
            cls = self.sections.set_index("name")['parser'].to_dict()[cls]
        for key in self.sections[self.sections['parser'] == cls].index.values:
            yield self.get_section(key)

    def _parse_1(self, parser, stops):
        """
        Wrapper for calling custom start parsing. The function
        :func:`~exa.core.parser.Parser._parse_start` is called.
        """
        return parser(self)._parse_start(stops)    # Does not copy lines

    def _parse_2(self, parser, starts):
        """
        Wrapper for calling custom end parsing. The function
        :func:`~exa.core.parser.Parser._parse_end` is called.
        """
        return parser(self)._parse_end(starts)     # Do not copy lines

    def _parse_3(self, parser):
        """
        Wrapper for calling custom start and end parsing. The function
        :func:`~exa.core.parser.Parser._parse_both` is called.
        """
        return parser(self)._parse_both()          # Ditto

    def _parse_start(self, stops):
        """
        Custom start parsing if needed (i.e. to be overwritten).

        Should return a list of 2-tuples of line number, line text pairs.

        .. code-block:: python

            [(i, self.lines[i]), (j, self.lines[j]), ...]
        """
        raise NotImplementedError("No implementation of _parse_start for {}".format(self.__class__))

    def _parse_end(self, starts):
        """
        Custom end parsing, if needed.

        Should return a list of 2-tuples of line number, line text pairs.

        .. code-block:: python

            [(i, self.lines[i]), (j, self.lines[j]), ...]
        """
        raise NotImplementedError("No implementation of _parse_end for {}".format(self.__class__))

    def _parse_both(self):
        """
        Custom start and end parsing, if needed.

        Should return two lists. Each list is a list of 2-tuples of line number,
        line text pairs. The first list is interpreted as start and the second
        as end points.

        .. code-block:: python

            ([(i, self.lines[i]), (j, self.lines[j]), ...],
             [(i, self.lines[i]), (j, self.lines[j]), ...])
        """
        raise NotImplementedError("No implementation of _parse_both for {}".format(self.__class__))

    @classmethod
    def add_parsers(cls, *parsers):
        """
        Add additional (section) parsers to the current parsing system.

        .. code-block:: python

            class P0(Parser):
                pass

            class P1(Parser):
                pass

            class Wrapper(Parser):
                pass

            Wrapper.add_parsers(P0, P1)    # Needs to be performed only once
            parser = Wrapper(myfile)
        """
        # A bit of deduplication is necessary
        def get(*parsers):
            dct = {}
            for p in parsers:
                if hasattr(p, "__module__"):
                    n = ".".join((p.__module__, p.__name__))
                else:
                    n = p.__name__
                dct[n] = p
            return dct

        if not hasattr(cls, "_parsers"):
            setattr(cls, "_parsers", [])
        current = get(*cls._parsers)
        new = get(*parsers)
        current.update(new)
        cls._parsers = list(current.values())

    def __init__(self, *args, **kwargs):
        super(Parser, self).__init__(*args, **kwargs)
        self.add_parsers(self.__class__)


#####
#value - CSV - files). Generally, the most difficult aspect of parsing such
#files (into appropriate data objects) is isolating the relevant text segment or
#segments. Once the text is isolated, an algorithm can usually be devised to
#create the appropriate in memory representation of the data for further
#manipulation, visualization, etc.
#
#This parsing is handled by :class:`~exa.core.parser.Parser`. Since those
#parsers require isolated text, machinery for automatic isolation of text is
#also provided in this module (:class:`~exa.core.parser.Sections`). These
#two classes work in tandem to facilitate parsing of text files like those
#described above. An example of how this works is given below.
#
#.. code-block:: text
#
#    # medium text file from some program
#    ...
#    # sysmetatic data to be parsed
#    -----------------
#    1.0    2.0    3.0
#    4.0    5.0    1.0
#    2.0    3.0    4.0
#    ...
#    -----------------
#    5.0    5.0    2.0
#    2.0    3.0    1.0
#    1.0    4.0    4.0
#    ...
#
#The elipsis in the example represent other sections that potentially contain
#data. Focusing only on the example given, data to be parsed is proceeded by
#some dashes. Asumming that a 'parsing' editor is created that contains only
#the lines below the dashes, parsing can be accomplished as follows.
#
#.. code-block:: python
#
#    from exa import Parser, TypedProperty, DataFrame
#
#    class DataBlock(Parser):
#        _names = ("A", "B", "C")    # Always 3 columns, named like this
#        data = TypedProperty(DataFrame, doc="block of data")
#
#        def _parse(self):
#            self.data = self.to_data(delim_whitespace=True, names=self._names)
#
#While this editor can be used directly (manually, see below), if multiple data
#sections exist (like in the text example above), it may be useful to hook this
#parser together with a sections identifier class that can parse all of the
#(sub) sections automatically.
#
#.. code-block:: python
#
#    # Manual usage of the DataBlock parser
#    myslice = "/path/to/sliced/text/file"    # Assume we manually sliced the text above
#    block = DataBlock(myslice)
#
#    # Here we build the sections
#
#    class DataFile(Sections):
#
#
#
#
#
#
#    class Data(Sections):
#        _key_sep = "^-+$"    # Regular expression to find section delimiters
#        _key_start = 0
#        _key_sp = 1
#
#        # This is the only method we need a concrete implementation for.
#        # It is responsible for populating the sections attribute.
#        def _parse(self):
#            # In parsing the sections we simply identify lines that contain
#            # only '----'
#            delimlines = self.regex(self._key_sep, text=False)[self._key_sep]
#            startlines = [self._key_start] + [delim + self._key_sp for delim in delimlines]
#            endlines = startlines[self._key_sp:]
#            endlines.append(len(self))
#            parsers = [Block]*len(startlines)    # Using the parser class above
#            # The ``sections`` attribute can be constructed this way
#            # or by hand.
#            self._sections_helper(parser=parsers, start=startlines, end=endlines)
#
#Now we have a modular and efficient parsing system for the prototypical text
#example above. Advanced machinery for lazy (automatic) parsing and additional
#triggering is possible via the ``TypedProperty`` function provided by
#:mod:`~exa.typed`. For examples see the tests of the aforementioned module and
#of this module (:mod:`~exa.tests.test_typed` and
#:mod:`~exa.core.tests.test_parser`).
#"""
##import six
##import warnings
##import numpy as np
##from abc import abstractmethod
##from .editor import Editor
##from .dataframe import SectionDataFrame
##from exa.typed import yield_typed, TypedProperty, TypedMeta
##
##
##class ParserMeta(TypedMeta):
##    """
##    Modified :class:`~exa.typed.TypedMeta` that additionally creates automatic
##    parsing functions for sections and data objects.
##
##    See Also:
##        :class:`~exa.typed.TypedMeta`
##    """
##    def __new__(mcs, name, bases, namespace):
##        clsdict = {}
##        prefix = namespace.pop("_getters", "_get")
##        if not isinstance(prefix, (list, tuple)):
##            prefix = (prefix, )
##        for attr_name, attr in namespace.items():
##            if isinstance(attr, TypedProperty):
##                for pref in prefix:
##                    # Create a function "_get_attrname" where "attrname" is some
##                    # attribute of interest. The function simply call self.parse()
##                    # so all parsing remains handled by the builtin .parse and
##                    # custom implemented ._parse methods.
##                    clsdict["_".join((pref, attr_name))] = lambda self: self.parse()
##                clsdict[attr_name] = attr(name=attr_name)
##            else:
##                clsdict[attr_name] = attr
##        return super(ParserMeta, mcs).__new__(mcs, name, bases, clsdict)
##
##
##class Parser(six.with_metaclass(ParserMeta, Editor)):
##    """
##    An editor-like object that is responsible for transforming a region
##    of text into an appropriate data object or objects.
##
##    This class can be used individually or in concert with the
##    :class:`~exa.core.parser.Sections` class to build a comprehensive parsing
##    system.
##
##    .. code-block:: python
##
##        import pandas as pd
##        from exa.typed import TypedProperty
##
##        text = '''comment1: 1
##        comment2: 2
##        comment3: 3'''
##
##        class MyParser(Parser):
##            comments = TypedProperty(list, doc="List of comments")
##            data = TypedProperty(pd.Series)
##            _key_d = ":"
##
##            def _parse(self):
##                comments = []
##                data = []
##                for line in self:
##                    comment, dat = line.split(self._key_d)
##                    comments.append(comment)
##                    data.append(dat)
##                self.data = data     # Automatic type conversion
##                self.comments = comments
##
##    See Also:
##        :class:`~exa.core.parser.Sections`
##    """
##    def parse(self, **kwargs):
##        """
##        Parse data objects from the current file.
##
##        Args:
##            verbose (bool): Performs a check for missing data objects
##        """
##        verbose = kwargs.pop("verbose", False)
##        self._parse()
##        if verbose:
##            for name, _ in yield_typed(self.__class__):
##                if not hasattr(self, name) or getattr(self, name) is None:
##                    warnings.warn("Missing data object {}".format(name))
##
##    @abstractmethod
##    def _parse(self, *args, **kwargs):
##        """
##        The parsing algorithm, specific to the text in question, should be
##        developed here. This function should assign the values of relevant
##        data objects based on the parsed text.
##        """
##        pass
##
##
##class Sections(six.with_metaclass(ParserMeta, Editor)):
##    """
##    An editor tailored to handling files with distinct regions of text.
##
##    A concrete implementation of this class provides the main editor-like
##    object that a user interacts with. This object's purpose is to identify
##    sections based on the structure of the text it is designed for. Identified
##    sections are automatically parsed. Sections may themselves be
##    :class:`~exa.core.parsing.Sections` objects (i.e. sub-sections).
##
##    The abstract method :func:`~exa.core.parser.Sections._parse` is used to
##    define the ``sections`` attribute, a dataframe containing, at a minimum,
##    section starting and ending lines, and the parser name (associated with a
##    :class:`~exa.core.parser.Sections` or :class:`~exa.core.parser.Parser`
##    object). An example ``sections`` table is given below with an optional
##    column, ``title``, used to aid the user in identifying sections.
##
##    +---------+-------------+---------------+-------+-----+
##    |         | parser      | title         | start | end |
##    +---------+-------------+---------------+-------+-----+
##    | section |             |               |       |     |
##    +---------+-------------+---------------+-------+-----+
##    | 0       | parser_name | Title  1      | 0     |  m  |
##    +---------+-------------+---------------+-------+-----+
##    | 1       | parser_name | Title  2      | m     |  n  |
##    +---------+-------------+---------------+-------+-----+
##
##    Attributes:
##        sections (DataFrame): Dataframe of section numbers, names, and starting/ending lines
##
##    See Also:
##        :class:`~exa.core.parser.Parser`
##    """
##    sections = TypedProperty(SectionDataFrame, "Parser sections")
##
###    @property
###    @abstractmethod
###    def fdelimiters(self):
###        """
###        Dictionary of delimiter keys, parser classes values identified by the
###        find method.
###
###        This property returns a dictionary of delimiter keys and Parser class
###        values. Since it is ambiguous whether the class parses the text after
###        or before the delimiter the convention is taken that class always
###        applies to the text after a delimiter. A special key, "__HEADER__", is
###        reserved for the text preceding the first delimiter instance.
###
###        .. code-block:: python
###
###            class Parser0(Parser):
###                def _parse(self):
###                    # Parse for some text segment
###
###            class Parser1(Parser):
###                def _parse(self):
###                    # Parse some other text segment
###
###            class MySections(Sections):
###                fdelimiters = {'__HEADER__': Parser0, '-----': Parser1}
###
###                # Alternatively can do
###                @property
###                def fdelimiters(self):
###                    return {'__HEADER__': Parser0, '-----': Parser1}
###
###        In the given example the only delimiter is "-----". ``Parser0`` handles
###        the text preceding the first instance of the delimiter. Text in between
###        (or simply after) the delimiters is parsed by ``Parser1``.
###        """
###        pass
###
###    @property
###    @abstractmethod
###    def rdelimiters(self):
###        """
###        Dictionary of delimiter keys, parser classes values identified by the
###        regex method.
###
###        See Also:
###            :func:`~exa.core.parser.Sections.fdelimiters`
###
###        Occasionally delimiters are found via regular expressions rather than
###        simple matching. This property behaves exactly as
###        :func:`~exa.core.parser.Sections.fdelimiters` except that delimiters
###        are identified via regular expression searches.
###        """
###        pass
##
##    def parse(self, recursive=False, verbose=False, **kwargs):
##        """
##        Parse the current file.
##
##        Args:
##            recursive (bool): If true, parses all sub-section/parser objects' data
##            verbose (bool): Print parser warnings
##            kwargs: Keyword arguments passed to parser
##        """
##        # This helper function is used to setup auto-parsing, see below.
##        def section_parser_helper(i):
##            def section_parser():
##                self.parse_section(i)
##            return section_parser
##        # Set the value of the ``sections`` attribute
##        self._parse(**kwargs)
##        if not hasattr(self, "_sections") or self._sections is None:
##            raise ValueError("Parsing method ``_parse`` does not correctly set ``sections``.")
##        # Now generate section attributes for the sections present
##        for i, sec in self.sections.iterrows():
##            parser, attrname = sec[['parser', 'attribute']]
##            if not isinstance(parser, type):
##                if verbose:
##                    warnings.warn("No parser for section '{}'!".format(parser.__class__))
##                # Default type is a simple editor
##                prop = TypedProperty(Editor)
##            else:
##                # Otherwise use specific sections/parser
##                prop = TypedProperty(parser)
##            # Now we perform a bit of class gymnastics:
##            # Because we don't want to attach our typed property paradigm
##            # (see exa.special.TypedProperty) to all instances of this
##            # object's class (note that properties must be attached to class
##            # definitions not instances of a class), we dynamically create a
##            # copy of this object's class, attach our properties to that
##            # class definition, and set it as the class of our current object.
##            cls = type(self)
##            if not hasattr(cls, '__unique'):
##                uniquecls = type(cls.__name__, (cls, ), {})
##                uniquecls.__unique = True
##                self.__class__ = uniquecls
##            # TypedProperty (prop) is LazyFunction so we evaluate it
##            # here and pass name since we know the name at this point.
##            setattr(self.__class__, attrname, prop(name=attrname))
##            # And attach a lazy evaluation method using the above helper.
##            # Again, see exa's documentation for more information.
##            setattr(self, "parse_" + attrname, section_parser_helper(i))
##            if recursive:
##                self.parse_section(i, recursive=True, verbose=verbose)
##
##    def parse_section(self, number, recursive=False, verbose=False, **kwargs):
##        """
##        Parse specific section of this object.
##
##        Parse section data can be accessed via the ``sectionID`` attribute, where
##        ID is the number of the section as listed in the ``describe_sections``
##        table or in the order given by the ``sections`` attribute.
##
##        Args:
##            number (int): Section number (of the ``sections`` list)
##            recursive (bool): Parse sub-section/parser objects
##            verbose (bool): Display additional warnings
##            kwargs: Keyword arguments passed to parser
##        """
##        parser, start, end, attrname = self.sections.loc[number, ["parser", "start", "end", "attribute"]]    # HARDCODED
##        if not isinstance(parser, type):
##            if verbose:
##                warnings.warn("No parser for section '{}'! Using generic editor.".format(parser.__name__))
##            sec = Editor(self[start:end], path_check=False)
##        else:
##            # Note that we don't actually parse anything until an
##            # attributed is requested by the user or some code...
##            sec = parser(self[start:end], path_check=False)
##        setattr(self, attrname, sec)
##        # ...except in the case recursive is true.
##        if recursive and hasattr(sec, "parse"):
##            # Propagate recursion
##            sec.parse(recursive=True, verbose=verbose, **kwargs)
##
##    def itersections(self):
##        """Iterate over each section object."""
##        for name in self.sections['attribute']:
##            yield self.get_section(name)
##
##    def get_section(self, section):
##        """
##        Select a section by (parser) name or section number.
##
##        Args:
##            section: Section number or parser name
##
##        Returns:
##            section_editor: Editor-like sections or parser object
##
##        Warning:
##            If multiple sections with the same parser name exist, selection must
##            be performed by section number.
##        """
##        inttypes = six.integer_types + (np.int, np.int8, np.int16, np.int32, np.int64)
##        if isinstance(section, six.string_types) and section.startswith("section"):
##            return getattr(self, section)
##        elif isinstance(section, six.string_types):
##            idx = self.sections[self.sections["parser"] == section].index.tolist()
##            if len(idx) > 1:
##                raise ValueError("Multiple sections with parser name {} found".format(section))
##            elif len(idx) == 0:
##                raise ValueError("No sections with parser name {} found".format(section))
##        elif isinstance(section, inttypes):
##            idx = section
##        else:
##            raise TypeError("Unknown type for section arg with type {}".format(type(section)))
##        idx = idx[0] if not isinstance(idx, inttypes) else idx
##        return getattr(self, str(self.sections.loc[idx, "attribute"]))
##
##    def _parse(self, **kwargs):
##        """
##        Systematic identification of regions of text
##        This abstract method is overwritten by a concrete implementation and is
##        responsible for setting the ``sections`` attribute.
##
##        Concrete implementations depend on the specific file. Note that the names
##        column of the dataframe must contain values corresponding to existing
##        parsers.
##
##        .. code-block:: python
##
##            class MySections(Sections):
##                def _parse(self):
##                    # This function should actually perform parsing
##                    names = [Parser0, Parser1]
##                    starts = [0, 10]
##                    ends = [10, 20]
##                    titles = ["A Title", "Another Title"]
##                    self._sections_helper(parsers, starts, ends, title=titles)
##        """
##        pass
##
##    def _sections_helper(self, parser, start, end, **kwargs):
##        """
##        Convenience method for building the ``sections`` attribute.
##
##        Automatically converts class types to string names.
##
##        .. code-block:: python
##
##            # End of the _parse() function
##            self._sections_helper(parsers, starts, ends, title=titles)
##        """
##        dct = {'parser': parser, 'start': start, 'end': end}
##        dct.update(kwargs)
##        self.sections = SectionDataFrame.from_dict(dct)
##
##
