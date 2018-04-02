# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Composers - ALPHA
####################################
This module provides an editor-like (:class:`~exa.core.editor.Editor`) class
that can be used to programmatically compose files. For many applications,
small to medium sized text files are used as inputs, parameter files, or config
files. The :class:`~exa.core.composer.Composer` is used to build such files.
"""
import re
from copy import copy
from exa.typed import Typed
from .editor import Editor


class Composer(Editor):
    """
    A specialized editor-like object for programmatically generating small/medium
    files from a given template.

    Special formatting strings cannot be positional. A new type of templating
    system is introduced for added flexibility. All special formatters not are
    considered optional; if no data is provided for them, the are removed upon
    composition. The follow documentation describes use and gives some examples.

    .. code-block:: python

        class MyComposer(Composer):
            # [name|indent|delimiter|qualifier|ending]
            template = '[key|0|=|'|]'

        c = MyComposer(key="value")
        c.compose()                # key='value'

        MyComposer.template = '[key|4|:||,]'
        c = MyComposer(key="value")
        c.compose()                #    key:value
        MyComposer.template = '[key|4| ||,]'
        c.compose()                #    key value,

    Note:
        Explicit vertical bar '|' characters, inside of special formatting strings,
        should be escaped (i.e. '\|') to be respected.

    Warning:
        The same criteria for named and positional formatters applies for the
        Composer as for all Python format strings.
    """
    # Regex for identifying special formatters [name|indent|delimiter|qualifier|ending]
    _regex = re.compile("\[([A-z0-9_]*?)\|(\d*?)\|(.*?)\|(.*?)\|(.*?)\]")
    _template = None
    _ignored = ("_args", "_cursor", "_lines", "nprint")
    args = Typed(tuple, doc="Positional template arguments")

    @property
    def _constructor(self):
        return Editor

    @property
    def template(self):
        return self._template

    def compose(self, *args, **kwargs):
        """
        Generate a file from the current template and given arguments.

        Warning:
            Make certain to check the formatted editor for correctness!

        Args:
            args: Positional arguments to update the template
            kwargs: Keyword arguments to update the template

        Returns:
            editor: An editor containing the formatted template.
        """
        linebreak = kwargs.pop("linebreak", "\n")
        # Update the internally stored args/kwargs from which formatting arguments come
        if len(args) > 0:
            self.args = args
        self._update(**kwargs)
        # Format string arguments (for the modified template)
        fkwargs = {}    # Format string keyword arguments
        modtmpl = []    # The modified template lines
        #curpos = 0      # Positional argument counter
        #i = 0
        for line in self:
            cline = copy(line)
            # If any special formatters exist, handle them
            for match in self._regex.findall(line):
                search = "[{}]".format("|".join(match))
                name, indent, delim, qual, _ = match
                if indent != "":
                    indent = " "*int(indent)
                delim = delim.replace("\\|", "|")
                # Collect and format the data accordingly
                data = getattr(self, name, None)
                # If no data exists, treat as optional
                if data is None:
                    cline = cline.replace(search, "")
                    continue
                elif delim.isdigit():
                    fkwargs[name] = getattr(self, "_fmt_"+name)()
                else:
                    fkwargs[name] = linebreak.join([indent+k+delim+qual+v+qual for k, v in data.items()])
                cline = cline.replace(search, "{"+name+"}")
            modtmpl.append(cline)
        modtmpl = "\n".join(modtmpl)
        print(modtmpl)
        dct = self.get_kwargs()
        dct.update(fkwargs)
        return self._constructor(textobj=modtmpl.format(*self.args, **dct))

    def get_kwargs(self):
        """Return kwargs from attached attributes."""
        return {k: v for k, v in vars(self).items() if k not in self._ignored}

    def _update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __init__(self, *args, **kwargs):
        """
        Protected init keywords are 'textobj', 'encoding', 'nprint', and
        'ignore'. For more information see :class:`~exa.core.editor.Editor`.
        """
        # The gymnastics below is required to support slicing of composers.
        textobj = kwargs.pop("textobj", None)
        if textobj is None:
            if self.template is None:
                raise TypeError("Composers require a template ('textobj' argument or '_template' attribute)!")
            else:
                textobj = self.template
        encoding = kwargs.pop("encoding", None)
        nprint = kwargs.pop("nprint", 15)
        ignore = kwargs.pop("ignore", False)
        super(Composer, self).__init__(textobj, encoding, nprint, ignore)
        self.args = args
        self._update(**kwargs)
