# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Parsers
####################################
"""
import six
import warnings
import pandas as pd
from abc import abstractmethod
from exa.special import yield_typed
from .editor import Editor
from .sections import SectionsMeta, Mixin


class Parser(six.with_metaclass(SectionsMeta, Editor, Mixin)):
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
    name = None        # Set by subclass
    description = None # ditto

    @abstractmethod
    def _parse(self, *args, **kwargs):
        """
        The parsing algorithm, specific to this section, belongs here.

        This function should set all data object attributes as defined by in
        the corresponding metaclass (e.g. :class:`~exa.core.editor.SectionsMeta`).

        See Also:
            An example implementation can be found in the docs of
            :class:`~exa.core.editor.Sections`.
        """
        pass

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

    @classmethod
    def describe_data(cls):
        """Description of data attributes associated with this parser."""
        df = {}
        for name, types in yield_typed(cls):
            df[name] = (cls._descriptions[name], types)
        df = pd.DataFrame.from_dict(df, orient='index')
        df.columns = ["description", "type"]
        df.index.name = "attribute"
        return df
