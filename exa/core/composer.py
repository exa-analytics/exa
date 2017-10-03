# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Composers
####################################
This module provides an editor-like (:class:`~exa.core.editor.Editor`) class
that can be used to programmatically compose files. For many applications,
small to medium sized text files are used as inputs, parameter files, or config
files. The :class:`~exa.core.composer.Composer` is used to build such files.
"""
import re
import string
from .editor import Editor
from exa.typed import Typed
_fmttr = string.Formatter()


class Composer(Editor):
    """
    A specialized editor-like object for programmatically generating small/medium files
    from a given template.

    Special formatting strings cannot be positional

    .. code-block:: python

        # Syntax of special formatters
        template = '[name | indent | delim | qual | ending]'
        # name: variable name (if named) otherwise integer for positional
        # kind: Predetermined formatting (see below)
        # indent: Line indent (in spaces)
        # ending: Line termination character(s)
        # required: Required argument, ('T', 't', '1') as true, ('F', 'f', '0') as false

        # kinds:
        # 0: Raw string (see _fmt0)
        # 1: Key, value pairs (space delimited, see _fmt1)
        # 2: Key, value pairs ('=' delimited, see _fmt2)
        # -1: Custom formatting function named '_cfmt1'
        # -2: Custom formatting function named '_cfmt2'
    """
    # Special formatters  [name,kind,indent,required,ending]
    _regex = re.compile("\[[A-z0-9_]+,[0-9-]*,\d*,[TtFf01],.*\]")
    _template = None
    _return_constructor = Editor    # Can be modified to return a different type
    args = Typed(tuple, doc="Positional template arguments")

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
        # Update the internally stored args/kwargs from which formatting arguments come
        if len(args) > 0:
            self.args = args
        self._update(**kwargs)
        # Format string arguments (for the modified template)
        fargs = []      # Format string positional arguments
        fkwargs = {}    # Format string keyword arguments
        curtmpl = []    # The modified template lines
        curpos = 0      # Positional argument counter
        i = 0
        for line in self:
            curtmpl.append(line)               # This will store our modified template
            for m in self._regex.finditer(line):    # If any special formatters exist
                match = m.group()
                # Hardcoded syntax (see "_regex")
                items = match[1:-1].replace(" ", "").split(",")
                # Check all the data
                if items[0] == "":                # name
                    name = curpos
                    curpos += 1
                else:
                    try:
                        name = int(items[0])
                    except ValueError:
                        name = items[0]
                if items[1] == "":                # kind
                    kind = 0
                else:
                    kind = int(items[1])
                if items[2] != "":                # indent
                    indent = " "*int(items[2])
                else:
                    indent = ""
                if items[3] in ["T", "t", "1"]:   # required
                    req = True
                else:
                    req = False
                ending = "".join(items[4:])       # ending
                # Collect the data from the composer
                # If the data is None, treat the special formatter
                # as optional; if there is nothing else on the line
                # remove it entirely, otherwise replace as empty
                if isinstance(name, int):
                    data = self.args[name]
                else:
                    data = getattr(self, name, None)
                if data is None:
                    if req == True:
                        raise ValueError("Required data '{}' missing!".format(name))
                    # If nothing else on line remove it from curtmpl
                    elif line.strip() == match.strip():
                        del curtmpl[-1]
                        i -= 1
                    else:
                        curtmpl[i] = curtmpl[i].replace(match, "")
                else:
                    curtmpl[i] = curtmpl[i].replace(match, "{" + str(name) + "}")
                    # Finally format the data object
                    fname = "_cfmt"+str(kind)[1:] if kind < 0 else "_fmt"+str(kind)
                    fkwargs[str(name)] = getattr(self, fname)(data, indent, ending)
            else:
                # Handle generic formatters
                for txt, fname, fmtspc, conv in _fmttr.parse(line):
                    if fname is None:
                        continue
                    if fname == "":
                        fargs.append(self.args[curpos])
                        curpos += 1
                    elif fname.isdigit():
                        fargs.append(self.args[int(fname)])
                    else:
                        fkwargs[fname] = getattr(self, fname)
            i += 1
        curtmpl = "\n".join(curtmpl)
        return curtmpl, fargs, fkwargs

    def _fmt_delim(self, dct, delim, indent, ending):
        """Generic formatter for arbitrary delimiters."""
        if indent != "" and ending != "":
            return "\n".join([indent+str(k)+delim+str(v)+ending for k, v in dct.items()])
        elif indent != "":
            return "\n".join([indent+str(k)+delim+str(v) for k, v in dct.items()])
        elif ending != "":
            return "\n".join([str(k)+delim+str(v)+ending for k, v in dct.items()])
        else:
            return "\n".join([str(k)+delim+str(v) for k, v in dct.items()])

    def _fmt1(self, dct, indent, ending):
        return self._fmt_delim(dct, " ", indent, ending)

    def _fmt2(self, dct, indent, ending):
        return self._fmt_delim(dct, " = ", indent, ending)

    def _update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __init__(self, textobj=None, encoding=None, nprint=15, *args, **kwargs):
        if self.template is textobj is None:
            raise TypeError("Composers require a template ('textobj' argument or '_template' attribute)!")
        elif textobj is None:
            textobj = self.template
        super(Composer, self).__init__(textobj, encoding, nprint)
        self.args = args
