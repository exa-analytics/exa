# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Parsing Editors
####################################
This module provides editors tailored to parsing small/medium sized text files
that do not have a consistent structure.
"""
import re
from .editor import Editor
from .data import DataFrame, Column, Index
from exa.typed import Typed


class Sections(DataFrame):
    """
    A representation of parts of specific parts of a file to be parsed.
    """
    section = Index(int)
    start = Column(int)
    stop = Column(int)
    parser = Column()
    _ed = Typed(Editor)

    @classmethod
    def from_lists(cls, start, stop, parser, ed):
        """
        Create a dataframe corresponding to sections of an editor.

        Args:
            start (array): Array of starting line numbers
            stop (array): Array of stopping line numbers
            parser (array): Array of parser classes for specific sections
        """
        df = cls.from_dict({'start': start, 'stop': stop, 'parser': parser})
        df._ed = ed
        return df

    def get_section(self, key):
        """
        Generate an editor corresponding to an identified section.

        Args:
            key (int): Integer corresponding to section

        Returns:
            ed (Editor): A correct editor/parser corresponding to the section
        """
        start, stop, cls = self.loc[key, ["start", "stop", "parser"]]
        return cls(self._ed.lines[start:stop])


class Parser(Editor):
    """
    An Editor-like object built for parsing small/medium files that are
    semi-structured.
    """
    _setters = ("parse", "_parse")
    _parsers = []
    _start = None
    _stop = None
    _0 = re.compile("^\s*$")
    sections = Typed(Sections)

    def parse_sections(self):
        """Identify sections of the file."""
        def selector(parser):
            """Do not perform redundant file searching."""
            for attrname in ("_start", "_stop"):
                attr = getattr(parser, attrname)
                if type(attr).__name__ == "SRE_Pattern":
                    regex.append(attr)
                elif isinstance(attr, str):
                    find.append(attr)
        # Start processing
        regex = []    # for .regex()
        find = []     # for .find
        selector(self)
        for parser in self._parsers:
            selector(parser)
        # Perform file searching
        rfound = self.regex(*regex)
        ffound = self.find(*find)
        # Identify sections
        startnums = []
        stopnums = []
        parsers = []
        for parser in self._parsers:
            if isinstance(parser._start, int):
                pass
            elif isinstance(parser._start, str):
                starts = ffound[parser._start]
            else:
                starts = rfound[parser._start]
            if isinstance(parser._stop, int):
                stops = self._parse_stops(parser._stop, starts)
            elif isinstance(parser._stop, str):
                stops = ffound[parser._stop]
            else:
                stops = rfound[parser._stop]
            startnums += [start[0] for start in starts]
            stopnums += [stop[0] + 1 for stop in stops]
            parsers += [parser]*len(starts)
        self.sections = Sections.from_lists(startnums, stopnums, parsers, self)

    def _parse_stops(self, which, *args, **kwargs):
        if which == 0:
            return self._parse_stops_0(*args, **kwargs)

    def _parse_stops_0(self, starts):
        stop = []
        for start in starts:
            self.cursor = start[0]
            found = self.regex_next(self._0)
            stop.append(found)
        return Matches(self._0, *stop)

    @classmethod
    def add_parsers(cls, *parsers):
        cls._parsers = list(set(cls._parsers + list(parsers)))



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
