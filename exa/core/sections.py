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
        # | Parser Name | Parameters | Class(es)        | Attributes          |
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

    def describe(cls):
        """Parser description."""
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

    +------------+-------------+-------+-----+
    | Section ID | Parser Name | Start | End |
    +------------+-------------+-------+-----+
    | 0          | default     | 0     | 1   |
    +------------+-------------+-------+-----+
    | 1          | default     | 2     | 3   |
    +------------+-------------+-------+-----+
    | 2          | default     | 4     | 5   |
    +------------+-------------+-------+-----+

    Attributes:
        sections (DataFrame): Dataframe of section numbers, names, titles, and starting/ending lines

    See Also:
        :class:`~exa.core.parser.Parser`
    """
    name = None        # Subclasses may set this if needed
    description = None # ditto
    _key_attr_prefix = "section"

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
                    names = ["first", "second"]
                    starts = [0, 10]
                    ends = [10, 20]
                    titles = [None, None]
                    self.sections =

                    self.sections = DataFrame.from_dict({"names": ["first", "sect

        """
        pass

    def _gen_sec_attr_name(self, i):
        """Generate section attribute name (e.g. section001)."""
        return self._key_sec_prefix + str(i).zfill(self._nsections)

    def parse(self, verbose=False):
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
                if verbose:
                    warnings.warn("No parser for section '{}'!".format(section))
                continue
            secname = self._gen_section_name(i)
            ptypes = self._parsers[section]
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
            setattr(self.__class__, secname, create_typed_attr(secname, ptypes))
            # And attach a lazy evaluation method using the above helper
            setattr(self, "parse_" + secname, section_parser_helper(i))

    def parse_all_sections(self, verbose=False):
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
        self.parse(verbose=verbose)
        for i in range(self._nsections):
            self.parse_section(i, recursive=True, verbose=verbose)

    def parse_section(self, number, recursive=False, verbose=False):
        """
        Parse specific section of this object.

        Parse section data can be accessed via the ``sectionID`` attribute, where
        ID is the number of the section as listed in the ``describe_sections``
        table or in the order given by the ``sections`` attribute.

        Args:
            number (int): Section number (of the ``sections`` list)
            recursive (bool): Parse all (possible) sub-sections

        See Also:
            Two very useful functions, :func:`~exa.core.editor.Sections.describe_sections`
            and :func:`~exa.editor.Sections.describe_parsers` show section names
            and numbers, and section parsers, respectively.
        """
        section, start, end = self.sections[number]
        if section not in self._parsers:
            if verbose:
                warnings.warn("No parser for section '{}'!".format(section))
            return
        secname = self._key_sec_prefix + str(number).zfill(self._nsections)
        # Note that we don't actually parse anything until a value is in fact
        # request, e.g. sections.parser.dataobj
        sec = self._parsers[section](self[start:end], path_check=False)
        setattr(self, secname, sec)
        if hasattr(sec, "parse_all_sections") and recursive:
            getattr(self, secname).parse_all_sections()
        else:
            getattr(self, secname).parse()

    def delimiters(self):
        """Describes the patterns used to disambiguate regions of the file."""
        return [(name, getattr(self, name)) for name in vars(self) if name.startswith("_key_")]

    def get_section(self, i):
        """Retrieve a section by name or number."""
        n = len(str(len(self.sections)))
        if isinstance(i, int):
            name = self._key_sec_prefix + str(i).zfill(n)
        else:
            name = []
            for j, nam in enumerate(self.sections):
                if i in nam:
                    name.append(self._key_sec_prefix + str(j).zfill(n))
            if len(name) > 1:
                raise ValueError("Multiple sections with name = {}".format(i))
            name = name[0]
        return getattr(self, name)

    def describe_sections(self):
        """
        Display available section names and numbers.

        Note:
            This method only has meaning once sections have been parsed.
        """
        if len(self.sections) == 0:
            warnings.warn("No sections identified.")
        else:
            df = pd.DataFrame(self.sections, columns=["Parser Name", "Start", "End"])
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

        .. code-block:: python

            Sections.add_section_parsers(Section1, Section2, ...)
        """
        cls._parsers.update({str(s.name): s for s in args})
        cls._parsers.update(kwargs)
