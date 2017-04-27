# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Parsing Editors
####################################
This module provides editors specifically tailored to parsing text files that
have distinct, typically repeating, regions. The paradigm followed here is to
divide up regions of text until the minimal unit of text is sliced. Each unit
of text has a dedicated class object associated with it. The class associated
with the smallest unit of text performs conversion from text to the appropriate
data object.

Given the following example text,

.. code-block:: text

    42.0 42.0 42.0
    --------------
    42.0 42.0 42.0
    --------------
    42.0 42.0 42.0

a concrete :class:`~exa.core.parsing.Sections` implementation may be as follows.

.. code-block:: python

    class DataSections(Sections):
        description = "Parses files with sections delimited by -"
        _key_sep = "^-+$"    # Regular expression to find section delimiters
        _key_start = 0       # We make all parsing parameters ``_key_\*``
        _key_sp = 1          # attributes so that ``describe`` methods
        _key_parser_name = "default"

        # This is the only method we need a concrete implementation for.
        # It is responsible for populating the sections attribute.
        # We use the ``_sections_builder`` function to help build the
        # ``sections`` attribute.
        def _parse(self):
            delimlines = self.regex(self._key_sep, text=False)[self._key_sep]
            startlines = [self._key_start] + [delim + self._key_sp for delim in delimlines]
            endlines = startlines[1:]
            endlines.append(len(self))
            parser_names = [self._key_parser_name]*len(startlines)
            dct = {'start': startlines, 'end': endlines, 'parser': parser_names}
            self._section_builder(dct)

This example will only identify sections, actual parsing to data objects is
performed by another object. Because each section, identified above, has the
same format, only a single 'parser' object is needed.

.. code-block:: python

    import six    # Useful for Python 2 compatibility
    import numpy as np

    class DataParserMeta(Meta):
        # This metaclass defines the data objects present in the parser
        array = np.ndarray   # Variable name 'array', type is numpy array
        _descriptions = {'array': "Data array"}  # Optional data description

    class DataParser(six.with_metaclass(DataParserMeta, Parser)):
        name = "default"    # This should match what we wrote above in DataSections
        description = "Parses data array sections of a file delimited by -"

        # This is the only method we need to define to make this concrete
        def _parse(self):
            # This function should set all data objects specified in the metaclass.
            # Note that type conversion, where possible, happens automatically
            # because we are using the special metaclass Meta.
            # Also, note that the text slice of 'self' is defined by the [start, end)
            # line numbers specified by the sections object above.
            self.array = str(self).split()

    # Last thing to do is to add the parser to the appropriate sections object
    DataSections.add_sections_parser(DataParser)

Now we have a modular and efficient parsing system for the prototypical text
example above. An advanced feature of these classes is the ability to combine
individual section data into combined data objects. For example, if all sections
delimited by '-' in fact belong to the same 'data space', the the ``DataSections``
object could look as follows.

.. code-block:: python

    import six
    import numpy as np

    class DataSectionsMeta(Meta):
        # Define the combined data object here
        matrix = np.ndarray

    class DataSections(Sections):
        # All the same as above plus the following
        # ...
        def _get_matrix(self):
            # This function utilizes an advanced feature of the Meta class
            # that allows automatic (lazy) generation of composite objects
            # such as the matrix object which is made from all of the parsed
            # sections' data.
            # This is pandas syntax (since sections is a DataFrame)
            default_sections = self.sections[self.sections['parser'] == "default"]
            self.matrix = [self.get_section(i).array for i in default_sections.index]

The `_get_matrix` function is automatically called when the matrix data object
is requested on the DataSections instance. A number of very useful methods can
help describe complex structures of parsing editors.

.. code-block:: python

    sections = Sections()
    sections.describe()           # Describes the sections object
    sections.describe_parsers()   # Describe available parsing editors
    sections.describe_data()      # Display available data objects

    parser = Parser()
    parser.describe()             # Description of the parser/parsing algorithm parameters
    parser.describe_data()        # Display parsed data attributes

Warning:
    Parsers should be added to sections class objects using the
    :func:`~exa.code.editor.Sections.add_section_parsers` function. Parser
    objects have a ``name`` attribute to identify what section they parse.
"""
import six
import warnings
import numpy as np
import pandas as pd
from abc import abstractmethod
from exa.special import simple_function_factory, yield_typed, create_typed_attr
from .base import ABCBaseMeta
from .editor import Editor


class Meta(ABCBaseMeta):
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
        return super(Meta, mcs).__new__(mcs, name, bases, clsdict)


class Mixin(object):
    """
    Mixin object for :class:`~exa.core.sections.Sections` and
    :class:`~exa.core.parser.Parser`.
    """
    name = None        # Set by subclass

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

    @classmethod
    def describe_data(cls):
        """Description of data attributes associated with this parser."""
        df = {}
        for name, types in yield_typed(cls):
            df[name] = (cls._descriptions[name], types)
        if len(df) == 0:
            df = pd.DataFrame([[0, 0]])    # Empty dataframe
            df = df[df[0] != 0]            # with columns as below
        else:
            df = pd.DataFrame.from_dict(df, orient='index')
        df.columns = ["description", "type"]
        df.index.name = "attribute"
        return df


class Sections(six.with_metaclass(Meta, Editor, Mixin)):
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
    |         | parser      | title         | start | end |
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
        # HARDCODED
        df['attribute'] = [self._section_name_prefix+str(i).zfill(len(str(len(df)))) for i in df.index]
        df = df.loc[:, list(self._sections_columns) + list(set(df.columns).difference(self._sections_columns))]
        df.index.name = self._section_name_prefix
        self.sections = df

    def _describe_data(self, data=[], inplace=False, section=None):
        """
        """
        df = self.describe_data().reset_index()
        df["parser"] = self.__class__.name
        if section is None:
            try:
                section = [name for name, var in globals().items() if var is self][0]
            except:
                section = "null"
            df["section"] = section
        data.append(df[df["attribute"] != "sections"])
        for i in self.sections.index:
            sec = self.get_section(i)
            section += "." + self.sections.loc[i, "attribute"]
            if sec is not None:
                sec._describe_data(data, True, section)
        if not inplace:
            data = pd.concat(data, ignore_index=True)
            return data.loc[:, ["section", "attribute", "parser", "description", "type"]]

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
            secname, attrname = self.sections.loc[i, ["parser", "attribute"]]    # HARDCODED
            if secname not in self._parsers and verbose:
                if verbose:
                    warnings.warn("No parser for section '{}'!".format(secname))
            else:
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
        secname, start, end, attrname = self.sections.loc[number, ["parser", "start", "end", "attribute"]]    # HARDCODED
        if secname not in self._parsers:
            if verbose:
                warnings.warn("No parser for section '{}'! Using generic editor.".format(secname))
            sec = Editor(self[start:end], path_check=False)
        else:
            # Note that we don't actually parse anything until a value is in fact
            # request, e.g. sections.parser.dataobj...
            sec = self._parsers[secname](self[start:end], path_check=False)
        setattr(self, attrname, sec)
        # ...or if recursive is true.
        if recursive and hasattr(sec, "parse"):
            sec.parse(recursive=True, verbose=verbose)

    def delimiters(self):
        """Describes the patterns used to disambiguate regions of the file."""
        return [(name, getattr(self, name)) for name in vars(self) if name.startswith("_key_")]

    def get_section(self, section):
        """
        Select a section by (parser) name or section number.

        Args:
            section: Section number or parser name

        Returns:
            section_editor: Editor-like sections or parser object

        Warning:
            If multiple sections with the same parser name exist, selection must
            be performed by section number.
        """
        if isinstance(section, six.string_types):
            idx = self.sections[self.sections["parser"] == section].index
            if len(idx) > 1:
                raise ValueError("Multiple sections with parser name {} found".format(section))
            idx = idx[0]
        elif isinstance(section, six.integer_types + (np.int, np.int8, np.int16, np.int32, np.int64)):
            idx = section
        else:
            raise TypeError("Unknown type for section arg with type {}".format(type(section)))
        try:
            return getattr(self, self.sections.loc[idx, "attribute"])
        except AttributeError:
            return None

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
        for s in args:
            if s.name is None:
                kwargs[s.__class__.__name__] = s
            else:
                kwargs[s.name] = s
        cls._parsers.update(kwargs)


class Parser(six.with_metaclass(Meta, Editor, Mixin)):
    """
    An editor like object that corresponds to a specific and distinct region of
    a file and contains parsing functionality tailored to this region. The
    :class:`~exa.core.editor.Parser` object can be used standalone or in concert
    with the :class:`~exa.core.editor.Sections` object for parsing of complex
    files with multiple regions.

    See Also:
        :class:`exa.core.editor.Sections`

    Warning:
        Subclasses must set the class attribute 'name' as the parser name.
    """
    description = None # ditto

    @abstractmethod
    def _parse(self, *args, **kwargs):
        """
        The parsing algorithm, specific to this section, belongs here.

        This function should set all data object attributes as defined by in
        the corresponding metaclass (e.g. :class:`~exa.core.editor.Meta`).

        See Also:
            An example implementation can be found in the docs of
            :class:`~exa.core.editor.Sections`.
        """
        pass

    def _describe_data(self, data=[], inplace=False, section=None):
        df = self.describe_data().reset_index()
        df["parser"] = self.__class__.name
        df["sectionid"] = section
        data.append(df)
        if not inplace:
            return pd.concat(data, ignore_index=True)

    def parse(self, **kwargs):
        """
        Parse data objects from the current file.

        Args:
            verbose (bool): Performs a check for missing data objects

        See Also:
            To see what data objects get populated, see
            :func:`~exa.core.parser.Parser.describe_data`.
        """
        verbose = kwargs.pop("verbose", False)
        self._parse()
        if verbose:
            for name, _ in yield_typed(self.__class__):
                if not hasattr(self, name) or getattr(self, name) is None:
                    warnings.warn("Missing data object {}".format(name))
