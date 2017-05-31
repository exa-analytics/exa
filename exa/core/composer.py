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
import six
from .parser import Meta, Parser
from .dataframe import Composition


class ComposerMeta(Meta):
    """Used to define
    """
    composition = Composition
    _descriptions = {'composition': "Template description",
                     '_template': "Template"}


class Composer(six.with_metaclass(ComposerMeta, Parser)):
    """
    An editor like object used to dynamically build text files of predetermined
    structure with data values coming from Python objects. A simple use case is
    as follows. Note that the special class variable ``_template`` is used.

    .. code-block:: python

        class SimpleComposer(Composer):
            _template = "{}\n{labeled}"

        comp = SimpleComposer(1, labeled="one")
        comp.compose()    # Renders "1\none"
    """
    _key_d0 = ":"
    _key_d1 = ","
    _key_n = "n"
    _key_nl = "\n"
    _key_bl = " "
    _template = None

    def compose(self):
        """
        Compose the editor.

        Automatically format the composer using the data objects.

        See Also:
            The :attr:`~exa.core.composer.Composition.composition` provides
            information about the template.
        """
        dct = vars(self)
        fmts = {}
        for _, row in self.composition.iterrows():
            name = row['name']
            length = row['length']
            if name in dct:
                val = dct[name]
                if isinstance(val, (tuple, list)):
                    val = row['joiner'].join([str(v) for v in val])
                elif isinstance(val, dict):
                    j = row['joiner']
                    val = [k + j + v for k, v in val.items()]
                    if length == self._key_n:
                        val = self._key_nl.join(val)
                    else:
                        val = self._key_bl.join(val)
            else:
                val = ""
            fmts[name] = val
        return self.format(*self._args, **fmts)

    def format(self, *args, **kwargs):
        """
        Format the composer.
        """
        inplace = kwargs.pop("inplace", False)
        text = str(self)
        for tmpl in self.templates:
            if self._key_d0 in tmpl:
                text = text.replace(tmpl, tmpl.split(self._key_d0)[-1])
        text = text.format(*args, **kwargs)
        if inplace:
            self._lines = text.splitlines()
        else:
            cp = self.copy()
            cp._lines = text.splitlines()
            return cp

    def _parse(self):
        """Build the composition object which describes the template."""
        lengths = []
        joiners = []
        names = []
        for tmpl in self.templates:
            try:
                length, joiner, name = tmpl.split(self._key_d0)
            except:
                name = tmpl
                length = 1
                joiner = ""
            lengths.append(length)
            joiners.append(joiner)
            names.append(name)
        self.composition = Composition.from_dict({'length': lengths,
                                                  'joiner': joiners,
                                                  'name': names})

    def __init__(self, data=None, *args, **kwargs):
        # Modify the first argument if a default template is provided
        if self._template is not None:
            if data is not None:
                args = (data, ) + args
            data = self._template
        super(Composer, self).__init__(data, *args, **kwargs)

    def __repr__(self):
        return self.compose()    # Implicit call repr call to type of render()
