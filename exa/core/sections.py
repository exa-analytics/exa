# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Sections Editor
####################################
A special type of editor targeted at facilitating parsing of text files with
repeating structure. In combination with :class:`~exa.core.parsers.Parser`s,
efficient objects for parsing can be created.

.. code-block:: python

    import six

    text = '''some
    --------------
    structured
    --------------
    text
    '''

    class MySections(Sections):
        name = "example_sections_parser"
        description = "Parses files separated by ---"
        _key_sep = "---"                # Arbitrary section separator
        _key_def_sec_name = "default"   # Section name

        def _parse(self):
            # The code below depends on the file in question
            delims = self.find(self._key_sep, which='lineno')[self._key_sep]
            starts = [delim + 1 for delim in delims]
            starts.insert(0, 0)
            ends = delims
            ends.append(len(self))
            names = [self._key_def_sec_name]*len(starts)
            self.sections = list(zip(names, starts, ends))

    class MyParserMeta(SectionsMeta):
        # The metaclass defines the parser's data objects and types
        wordcount = int
        wordlist = list
        _descriptions = {'wordcount': "Count of number of words",
                         'wordlist': "List of words"}

    class MyParser(six.with_metaclass(MyParserMeta, Parser)):
        # This is a class that parsers the specific section (region)
        description = "Parser for individual region separated by -* regex"
        name = "default"

        def _parse(self):
            # Arbitrary what data objects are created here
            self.wordlist = [word for line in self.lines for word in line.split()]
            self.wordcount = len(self.wordlist)

    # The following needs only be performed once,
    # preferably at the module level, hidden from the user.
    MySections.add_section_parsers(MyParser)

    # The following shows some useful commands and (commented) print output
    # Prior to using a Sections or Section object one can inspect them
    MySections.describe()
        # Class          <class '...'>
        # Description    Parses files separated by -* regex
        # Name                      example_sections_parser
        # Parameters                    [sep, def_sec_name]

    MySections.describe_parsers()
        # +-------------+------------+------------------+---------------------+
        # | Parser Name | Parameters | Class(es)        | attributes          |
        # +-------------+------------+------------------+---------------------+
        # | default     | None       | <class 'Parser'> | wordcount, wordlist |
        # +-------------+------------+------------------+---------------------+

    # The object is create just like all editors
    edit = MySections(text)
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

See Also:
    :mod:`~exa.core.parsers`

Warning:
    Parsers should be added to sections class objects using the
    :func:`~exa.code.editor.Sections.add_section_parsers` function.
    Parser objects have a ``name`` attribute to identify what section they
    parse.
"""
import six
import warnings
import pandas as pd
from abc import abstractmethod
from exa.special import simple_function_factory, yield_typed, create_typed_attr
from .base import ABCBaseMeta
from .editor import Editor


class SectionsMeta(ABCBaseMeta):
    """
    Metaclass that automatically generates parsing function wrappers.

    Attributes:
        sections (list): A list of tuples of the form [(name, start, end), ...]
    """
    _descriptions = {"sections": "List of sections"}
    sections = pd.DataFrame

    def __new__(mcs, name, bases, clsdict):
        for attr in yield_typed(mcs):
            f = simple_function_factory("parse", "parse", attr[0])
            clsdict[f.__name__] = f
        clsdict['_descriptions'] = mcs._descriptions
        clsdict['_parsers'] = {}
        return super(SectionsMeta, mcs).__new__(mcs, name, bases, clsdict)


class Mixin(object):
    """
    Mixin object for :class:`~exa.core.sections.Sections` and
    :class:`~exa.core.parser.Parser`.
    """
    def describe(self):
        """Parser description."""
        data = {"name": self.name, "description": self.description,
                "type": "Sections" if isinstance(self, Sections) else "Parser"}
        params = [n.replace("_key_", "") for n in vars(self) if n.startswith("_key_")]
        if len(params) == 0:
            data["parameters"] = None
        else:
            data["parameters"] = params
        return pd.Series(data)


class Sections(six.with_metaclass(SectionsMeta, Editor, Mixin)):
    """
    An editor tailored to handling files with distinct regions of text.

    A concrete implementation of this class provides the main editor-like
    object that a user interacts with. This object's purpose is to identify
    sections of the text it contains. Identified sections can be automatically
    or manually parsed. Sections may themselves be :class:`~exa.core.sections.Sections`
    objects (i.e. 'subsections').

    The abstract method :func:`~exa.core.sections.Sections._parse` is used to
    define the ``sections`` attribute, a dataframe containing section numbers,
    names, titles, and starting/ending lines. Parsing objects are related by
    their names. Below is an example of the ``sections`` tables.

    +---------+-------------+---------------+-------+-----+
    |         | parser      | titlec        | start | end |
    +---------+-------------+---------------+-------+-----+
    | section |             |               |       |     |
    +---------+-------------+---------------+-------+-----+
    | 0       | parser_name | A Title       | 0     |  n  |
    +---------+-------------+---------------+-------+-----+

    Attributes:
        sections (DataFrame): Dataframe of section numbers, names, titles, and starting/ending lines

    See Also:
        :class:`~exa.core.parser.Parser`

    Note:
        Be careful modifying the :attr:`~exa.core.sections.Sections._sections_columns`
        attribute, the 'parser', 'start', and 'end' columns are hardcoded.
    """
    name = None        # Subclasses may set this if needed
    description = None # ditto
    _section_name_prefix = "section"
    _sections_columns = ("parser", "start", "end")

    @abstractmethod
    def _parse(self):
        """
        This abstract method is overwritten by a concrete implementation and is
        responsible for setting the ``sections`` attribute.

        Concrete implementations depend on the specific file. Note that the names
        column of the dataframe must contain values corresponding to existing
        parsers.

        .. code-block:: python

            class MySections(Sections):
                def _parse(self):
                    # This function should actually perform parsing
                    # and generate the sections object using the ``_sections_helper``.
                    names = ["parser_name", "other_parser"]
                    starts = [0, 10]
                    ends = [10, 20]
                    titles = ["A Title", "Another Title"]
                    dct = {"parser": names, "start": starts, "end": ends, "title": titles}
                    self._sections_helper(DataFrame.from_dict(dct))

        See Also:
            :func:`~exa.core.sections.Sections._sections_helper`
        """
        pass

    def _sections_helper(self, dct):
        """
        Sections dataframe creation helper.

        Args:
            dct (dict): Dictionary of parser names, section titles, starting lines, and ending lines
        """
        df = pd.DataFrame.from_dict(dct)
        for col in self._sections_columns:
            if col not in df:
                raise ValueError("Sections dataframe requires columns: {}".format(", ".join(self._sections_columns)))
        df[self._section_name_prefix] = [self._section_name_prefix+str(i).zfill(len(str(len(df)))) for i in df.index]
        df = df.loc[:, list(self._sections_columns) + list(set(df.columns).difference(self._sections_columns))]
        df.index.name = self._section_name_prefix
        self.sections = df

    def parse(self, recursive=False, verbose=False):
        """
        Parse the current file.

        Args:
            recursive (bool): If true, parses all sub-section/parser objects' data
            verbose (bool): Print parser warnings

        Tip:
            To see what objects exist, see the :attr:`~exa.core.sections.Sections.sections`
            attribute and :func:`~exa.core.sections.Sections.describe`,
            :func:`~exa.core.sections.Sections.describe_sections`, and
            :func:`~exa.core.sections.Sections.describe_parsers`.

        See Also:
            :func:`~exa.core.editor.Sections.parse_section`
        """
        # This helper function is used to setup auto-parsing, see below.
        def section_parser_helper(i):
            def section_parser():
                self.parse_section(i)
            return section_parser
        # Set the value of the ``sections`` attribute
        self._parse()
        if not hasattr(self, "sections") or self.sections is None:
            raise ValueError("Parsing method ``_parse`` does not correctly set ``sections``.")
        # Now generate section attributes for the sections present
        for i in self.sections.index:
            secname, attrname = self.sections.loc[i, ["parser", "section"]]    # HARDCODED
            if secname not in self._parsers:
                if verbose:
                    warnings.warn("No parser for section '{}'!".format(secname))
                continue
            ptypes = self._parsers[secname]
            # Now we perform a bit of class gymnastics:
            # Because we don't want to attach our typed property paradigm
            # (see exa.typed.create_typed_attr) to all instances of this
            # object's class, we dynamically create a copy of this object's
            # class and attach our properties to that class object.
            cls = type(self)
            if not hasattr(cls, '__unique'):
                uniquecls = type(cls.__name__, (cls, ), {})
                uniquecls.__unique = True
                uniquecls.add_section_parsers(*cls._parsers.values())
                self.__class__ = uniquecls
            setattr(self.__class__, attrname, create_typed_attr(attrname, ptypes))
            # And attach a lazy evaluation method using the above helper
            setattr(self, "parse_" + attrname, section_parser_helper(i))
            if recursive:
                self.parse_section(i, recursive=True, verbose=verbose)

    def parse_section(self, number, recursive=False, verbose=False):
        """
        Parse specific section of this object.

        Parse section data can be accessed via the ``sectionID`` attribute, where
        ID is the number of the section as listed in the ``describe_sections``
        table or in the order given by the ``sections`` attribute.

        Args:
            number (int): Section number (of the ``sections`` list)
            recursive (bool): Parse sub-section/parser objects
            verbose (bool): Display additional warnings

        Tip:
            To see what objects exist, see the :attr:`~exa.core.sections.Sections.sections`
            attribute and :func:`~exa.core.sections.Sections.describe`,
            :func:`~exa.core.sections.Sections.describe_sections`, and
            :func:`~exa.core.sections.Sections.describe_parsers`.
        """
        secname, start, end, attrname = self.sections.loc[number, ["parser", "start", "end", "section"]]    # HARDCODED
        if secname not in self._parsers:
            if verbose:
                warnings.warn("No parser for section '{}'!".format(section))
            return
        # Note that we don't actually parse anything until a value is in fact
        # request, e.g. sections.parser.dataobj...
        sec = self._parsers[secname](self[start:end], path_check=False)
        setattr(self, attrname, sec)
        # ...or if recursive is true.
        if recursive:
            sec.parse(recursive=True, verbose=verbose)
            #getattr(self, attrname).parse(recursive=True, verbose=verbose)

    def delimiters(self):
        """Describes the patterns used to disambiguate regions of the file."""
        return [(name, getattr(self, name)) for name in vars(self) if name.startswith("_key_")]

    def get_section(self, i):
        """Retrieve a section by name or number."""
        n = len(str(len(self.sections)))
        if isinstance(i, int):
            name = self._section_name_prefix + str(i).zfill(n)
        else:
            name = []
            for j, nam in enumerate(self.sections):
                if i in nam:
                    name.append(self._section_name_prefix + str(j).zfill(n))
            if len(name) > 1:
                raise ValueError("Multiple sections with name = {}".format(i))
            name = name[0]
        return getattr(self, name)

    @classmethod
    def describe_parsers(cls):
        """Display available section parsers."""
        data = {}
        for key, item in cls._parsers.items():
            params = len([n for n in vars(item) if n.startswith("_key_")])
            attrs = len([attr[0] for attr in yield_typed(item)])
            typ = "Sections" if item in Sections.__subclasses__() else "Parser"
            data[key] = (params, typ, attrs)
        if len(data) == 0:
            warnings.warn("No parsers added.")
        else:
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index.name = "parser"
            df.columns = ["key parameters", "type", "attributes"]
            return df

    @classmethod
    def add_section_parsers(cls, *args, **kwargs):
        """
        Add section parsers classes.

        .. code-block:: python

            Sections.add_section_parsers(Section1, Section2, ...)
        """
        cls._parsers.update({str(s.name): s for s in args})
        cls._parsers.update(kwargs)
