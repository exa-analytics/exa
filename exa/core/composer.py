# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Composers
####################################
Composers are editor like objects that are used to programmatically create
text files using a standard structure of template. This is akin to, for example,
JSON; the JSON library does not know a priori what data it will contain only
how to format whatever data it receives. Similarly, composers can be built
using a standard format or a template and have their data fields/values be
populated dynamically.
"""
from .editor import Editor
from .parser import Parser
from .dataframe import Composition
from exa.typed import cta


class Composer(Parser):
    """
    An editor like object used to dynamically build text files of predetermined
    structure with data values coming from Python objects. A simple use case is
    as follows. Note that the special class variable ``_template`` is used.

    .. code-block:: python

        class SimpleComposer(Composer):
            _template = "{}\n{labeled}"

        comp = SimpleComposer(1, labeled="one")
        comp.compose()    # Renders "1\none"

    Attributes:
        _key_d0 (str): First template delimiter
        _key_d1 (str): Second template delimiter
        _key_n (str): N-length identifier
        _key_nl (str): Newline joiner (N-length)
        _key_bl (str): Newline joiner (1-length)
        _key_dlen (int): Default template (line) length
        _key_djin (str): Default template joiner
    """
    _key_d0 = ":"
    _key_d1 = ","
    _key_n = "n"
    _key_nl = "\n"
    _key_bl = " "
    _key_dlen = 1
    _key_djin = ""
    composition = cta("composition", Composition, "Template description")

    def compose(self):
        """
        Compose the editor.

        Automatically format the composer using the data objects. The formatter
        works by iterating over the ``composition`` dataframe (a representation
        of the template) building the strings to be used in formatting the
        template. Positional arguments are taken from the special ``_args``
        attribute without modification.

        By default, only str, dict, list, and tuples types have composition
        functions: ``_compose_str``, ``_compose_list``, etc. Additional kw
        composition functions can added (or existing ones can be modified).

        .. code-block:: python

            class CmpsrMeta(ComposerMeta):
                myvar = str

            class Cmpsr(six.with_metaclass(CmpsrMeta, Composer):
                def _compose_str(self, value):
                    # Put single quotes around the value and do nothing else
                    return "'" + str(value) + "'"

        See Also:
            The :attr:`~exa.core.composer.Composition.composition` provides
            information about the template.
        """
        dct = vars(self)
        kws = {}
        # Dynamically identify available template composers
        composers = self._get_composers()
        # Iterate over the templates
        for _, row in self.composition.iterrows():
            name = row['name']    # Access using the property name
            pname = "_" + name    # and non-property name
            # If we don't have data to populate the template with...
            if name not in dct and pname not in dct:
                data = ""           # ...make it blank
            else:                   # Otherwise retrieve and compose it
                data = getattr(self, name)
                typname = type(data).__name__
                if typname in composers:
                    data = composers[typname](data, **row.to_dict())
                data = str(data)
            kws[name] = data
        return self.format(*self._args, **kws)

    def format(self, *args, **kwargs):
        """
        Format the composer.

        Args:
            args (tuple): Positional formatter arguments
            kwargs (dict): Keyword formatter arguments

        Note:
            Composers cannot be formatted 'inplace'; they always return a
            new :class:`~exa.core.editor.Editor` object.

        See Also:
            Typically composers automatically format their templates using the
            :func:`~exa.core.composer.Composer.compose` function.
        """
        text = self._preformat()
        text = self._format(text, *args, **kwargs)
        return self._postformat(text)

    def _preformat(self):
        """
        Generate the text representation of the current composer template.
        Requires modification of the non-standard template strings
        ('_exa_tmpl' format) to look like standard Python template strings.

        .. code-block:: python

            "{1:=:dct}"    # Special format template strings are converted
            "{dct}"        # to standard format strings
        """
        text = str(self)
        for tmpl in self.templates:
            if self._key_d0 in tmpl:
                text = text.replace(tmpl, tmpl.split(self._key_d0)[-1])
        return text

    def _format(self, text, *args, **kwargs):
        """
        This function, by default, behaves similarly to the default editor's
        format function but can be overwritten by subclasses if necessary. A
        common example is when additional logic is needed depending
        """
        return text.format(*args, **kwargs)

    def _postformat(self, text):
        """
        Called once formatting of the composer's template has completed and
        determines whether to build a new editor or modify the current one.
        """
        cp = Editor(self.copy())
        cp._lines = text.splitlines()
        return cp

    def _parse(self):
        """Build the composition object which describes the template."""
        # We need a parser for the template: the Composer editor's contents
        # is a template to be formatted by default. Python objects such as
        # lists and dicts (whatever is appropriate for the compositional task)
        # are what store the data that populates the template.
        lengths = []
        joiners = []
        names = []
        types = []
        for tmpl in self.templates:
            try:
                length, joiner, name = tmpl.split(self._key_d0)
            except:
                name = tmpl
                length = self._key_dlen
                joiner = self._key_djin
            try:
                dtype = getattr(self.__class__.__class__, name)
            except AttributeError:
                dtype = None
            lengths.append(length)
            joiners.append(joiner)
            names.append(name)
            types.append(dtype)
        dct = {'length': lengths, 'joiner': joiners, 'name': names, 'type': types}
        self.composition = Composition.from_dict(dct)

    def _get_composers(self):
        """Helper function to identify ``_compose_\*`` functions."""
        composers = {}
        for name in dir(self):
            if name.startswith("_compose_"):
                typ = name.split("_")[-1]
                composers[typ] = getattr(self, name)
        return composers

    def _compose_ordereddict(self, val, **kwargs):
        """Modify ordered dictionary keywords."""
        return self._compose_dict(val, **kwargs)

    def _compose_dict(self, val, **kwargs):
        """Modify dictionary keywords."""
        joiner = str(kwargs.pop("joiner", self._key_djin))
        length = kwargs.pop("length", self._key_dlen)
        lval = [str(k) + joiner + str(v) for k, v in val.items()]
        if length == "n":
            return self._key_nl.join(lval)
        return self._key_bl.join(lval)

    def _compose_list(self, val, **kwargs):
        """Modify list keywords."""
        joiner = str(kwargs.pop("joiner", self._key_djin))
        return joiner.join(val)

    def _compose_tuple(self, val, **kwargs):
        """Modify tuple keywords."""
        return self._compose_list(val, **kwargs)

    def _compose_str(self, val, **kwargs):
        """Modify list keywords."""
        return val

    def __init__(self, data=None, *args, **kwargs):
        # Modify the first argument if a default template is provided
        if data is None and self._lines is None:
            raise MissingTemplate()
        if self._template is not None:
            if data is not None:
                args = (data, ) + args
            data = self._template
        elif isinstance(data, str) and self._template is None:
            self._template = data
        super(Composer, self).__init__(data, *args, **kwargs)
