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
        _sep = "^-+$"    # Regular expression to find section delimiters
        _start = 0
        _sp = 1
        _parser_name = "DataParser"    # Class name of parser

        # This is the only method we need a concrete implementation for.
        # It is responsible for populating the sections attribute.
        def _parse(self):
            delimlines = self.regex(self._sep, text=False)[self._sep]
            startlines = [self._start] + [delim + self._sp for delim in delimlines]
            endlines = startlines[1:]
            endlines.append(len(self))
            parser_names = [self._parser_name]*len(startlines)
            dct = {'start': startlines, 'end': endlines, 'parser': parser_names}
            self._sections_helper(dct)

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
delimited by '-' belong to the same 'data space', the ``DataSections`` object
could look the following.

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
is requested on the ``DataSections`` instance. A number of very useful methods
can help describe complex structures of parsing editors.

.. code-block:: python

    ed = DataSections(text)       # Create the editor like object
    ed.sections                   # Display the sections dataframe
    ed.describe()                 # Describe available data objects
    ed.describe_parsers()         # Description of present parsers

    s0 = ed.section0              # Automatically generated subsection of type Parser
    s0.describe()                 # Display available data objects
"""
import six
import warnings
import numpy as np
from abc import abstractmethod
from .editor import Editor, EditorMeta
from .dataframe import SectionDataFrame
from exa.special import simple_function_factory, yield_typed, create_typed_attr


class SectionsMeta(EditorMeta):
    """
    Metaclass that automatically generates parsing function wrappers.

    Attributes:
        sections (list): A list of tuples of the form [(name, start, end), ...]
    """
    sections = SectionDataFrame
    _descriptions = {"sections": "Dataframe containing description of text regions"}

    def __new__(mcs, name, bases, clsdict):
        for attr in yield_typed(mcs):
            f = simple_function_factory("parse", "parse", attr[0])
            clsdict[f.__name__] = f
        clsdict['_descriptions'] = mcs._descriptions
        clsdict['_parsers'] = {}
        return super(SectionsMeta, mcs).__new__(mcs, name, bases, clsdict)


class Sections(six.with_metaclass(SectionsMeta, Editor)):
    """
    An editor tailored to handling files with distinct regions of text.

    A concrete implementation of this class provides the main editor-like
    object that a user interacts with. This object's purpose is to identify
    sections based on the structure of the text it is designed for. Identified
    sections are automatically parsed. Sections may themselves be
    :class:`~exa.core.parsing.Sections` objects (i.e. sub-sections).

    The abstract method :func:`~exa.core.parsing.Sections._parse` is used to
    define the ``sections`` attribute, a dataframe containing, at a minimum,
    section starting and ending lines, and the parser name (associated with a
    :class:`~exa.core.parsing.Sections` or :class:`~exa.core.parsing.Parser`
    object). An example ``sections`` table is given below with an optional
    column, ``title``, used to aid the user in identifying sections.

    +---------+-------------+---------------+-------+-----+
    |         | parser      | title         | start | end |
    +---------+-------------+---------------+-------+-----+
    | section |             |               |       |     |
    +---------+-------------+---------------+-------+-----+
    | 0       | parser_name | Title  1      | 0     |  m  |
    +---------+-------------+---------------+-------+-----+
    | 1       | parser_name | Title  2      | m     |  n  |
    +---------+-------------+---------------+-------+-----+

    Attributes:
        sections (DataFrame): Dataframe of section numbers, names, and starting/ending lines

    See Also:
        :class:`~exa.core.parsing.Parser`
    """
    def parse(self, recursive=False, verbose=False, **kwargs):
        """
        Parse the current file.

        Args:
            recursive (bool): If true, parses all sub-section/parser objects' data
            verbose (bool): Print parser warnings
            kwargs: Keyword arguments passed to parser

        Tip:
            Helpful methods for describing parsing and data are
            :attr:`~exa.core.parsing.Sections.sections`,
            :func:`~exa.core.parsing.Sections.describe`, and
            :func:`~exa.core.parsing.Sections.describe_parsers`.

        See Also:
            :func:`~exa.core.parsing.Sections.parse_section`
        """
        # This helper function is used to setup auto-parsing, see below.
        def section_parser_helper(i):
            def section_parser():
                self.parse_section(i)
            return section_parser
        # Set the value of the ``sections`` attribute
        self._parse(**kwargs)
        if not hasattr(self, "_sections") or self._sections is None:
            raise ValueError("Parsing method ``_parse`` does not correctly set ``sections``.")
        # Now generate section attributes for the sections present
        for i in self.sections.index:
            secname, attrname = self.sections.loc[i, ["parser", "attribute"]]    # HARDCODED
            if secname not in self._parsers:
                if verbose:
                    warnings.warn("No parser for section '{}'!".format(secname))
                # Default type is a simple editor
                prop = create_typed_attr(attrname, Editor)
            else:
                # Otherwise use specific sections/parser
                ptypes = self._parsers[secname]
                prop = create_typed_attr(attrname, ptypes)
            # Now we perform a bit of class gymnastics:
            # Because we don't want to attach our typed property paradigm
            # (see exa.special.create_typed_attr) to all instances of this
            # object's class (note that properties must be attached to class
            # definitions not instances of a class), we dynamically create a
            # copy of this object's class, attach our properties to that
            # class definition, and set it as the class of our current object.
            cls = type(self)
            if not hasattr(cls, '__unique'):
                uniquecls = type(cls.__name__, (cls, ), {})
                uniquecls.__unique = True
                uniquecls.add_section_parsers(*cls._parsers.values())
                self.__class__ = uniquecls
            setattr(self.__class__, attrname, prop)
            # And attach a lazy evaluation method using the above helper.
            # Again, see exa's documentation for more information.
            setattr(self, "parse_" + attrname, section_parser_helper(i))
            if recursive:
                self.parse_section(i, recursive=True, verbose=verbose)

    def parse_section(self, number, recursive=False, verbose=False, **kwargs):
        """
        Parse specific section of this object.

        Parse section data can be accessed via the ``sectionID`` attribute, where
        ID is the number of the section as listed in the ``describe_sections``
        table or in the order given by the ``sections`` attribute.

        Args:
            number (int): Section number (of the ``sections`` list)
            recursive (bool): Parse sub-section/parser objects
            verbose (bool): Display additional warnings
            kwargs: Keyword arguments passed to parser

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
            sec.parse(recursive=True, verbose=verbose, **kwargs)

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
        inttypes = six.integer_types + (np.int, np.int8, np.int16, np.int32, np.int64)
        if isinstance(section, six.string_types) and section.startswith("section"):
            return getattr(self, section)
        elif isinstance(section, six.string_types):
            idx = self.sections[self.sections["parser"] == section].index.tolist()
            if len(idx) > 1:
                raise ValueError("Multiple sections with parser name {} found".format(section))
            elif len(idx) == 0:
                raise ValueError("No sections with parser name {} found".format(section))
        elif isinstance(section, inttypes):
            idx = section
        else:
            raise TypeError("Unknown type for section arg with type {}".format(type(section)))
        idx = idx[0] if not isinstance(idx, inttypes) else idx
        return getattr(self, str(self.sections.loc[idx, "attribute"]))

    @classmethod
    def add_section_parsers(cls, *args, **kwargs):
        """
        Add section parsers classes.

        .. code-block:: python

            Sections.add_section_parsers(Section1, Section2, ...)
        """
        for s in args:
            kwargs[s.__name__] = s
        cls._parsers.update(kwargs)

    @abstractmethod
    def _parse(self, **kwargs):
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
                    names = ["ParserName", "OtherParser"]
                    starts = [0, 10]
                    ends = [10, 20]
                    titles = ["A Title", "Another Title"]
                    self._sections_helper(parsers, starts, ends, title=titles)
        """
        pass

    def _sections_helper(self, parser, start, end, **kwargs):
        """
        Convenience method for building the ``sections`` object.

        Automatically converts class types to string names.

        .. code-block:: python

            # End of the _parse() function
            self._sections_helper(parsers, starts, ends, title=titles)
        """
        parser = [par.__name__ if isinstance(par, type) else par for par in parser]
        dct = {'parser': parser, 'start': start, 'end': end}
        dct.update(kwargs)
        self.sections = SectionDataFrame.from_dict(dct)


class ParserMeta(EditorMeta):
    """Default metaclass for the Parser object."""
    _descriptions = {}

    def __new__(mcs, name, bases, clsdict):
        for attr in yield_typed(mcs):
            f = simple_function_factory("parse", "parse", attr[0])
            clsdict[f.__name__] = f
        clsdict['_descriptions'] = mcs._descriptions
        return super(ParserMeta, mcs).__new__(mcs, name, bases, clsdict)


class Parser(six.with_metaclass(ParserMeta, Editor)):
    """
    An editor-like object that is responsible for transforming a system region
    of text into an appropriate data object or objects.

    This object can be used standalone to handle parsing of a single file or in
    combination with the :class:`~exa.core.parsing.Sections` object to build a
    comprehensive but modular parsing system. The latter works best for large
    files containing (repeating) distinct sections.

    .. code-block:: text

    See Also:
        :class:`exa.core.parsing.Sections`
    """
    def parse(self, **kwargs):
        """
        Parse data objects from the current file.

        Args:
            verbose (bool): Performs a check for missing data objects

        See Also:
            To see what data objects get populated, see
            :func:`~exa.core.parsing.Parser.describe`.
        """
        verbose = kwargs.pop("verbose", False)
        self._parse()
        if verbose:
            for name, _ in yield_typed(self.__class__):
                if not hasattr(self, name) or getattr(self, name) is None:
                    warnings.warn("Missing data object {}".format(name))

    @abstractmethod
    def _parse(self, *args, **kwargs):
        """
        The parsing algorithm, specific to this section, belongs here.

        This function should set all data object attributes as defined by in
        the corresponding metaclass (e.g. :class:`~exa.core.parsing.Meta`).

        See Also:
            An example implementation can be found at :mod:`~exa.core.parsing`.
        """
        pass
