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





#from copy import copy, deepcopy
#from .editor import Editor
#from .parser import Parser
#from .dataframe import Composition
#from exa.typed import TypedProperty
#
#
#class Composer(Parser):
#    """
#    An editor like object used to dynamically build text files of predetermined
#    structure with data values coming from Python objects. A simple use case is
#    as follows. Note that the special class variable ``_template`` is used.
#
#    .. code-block:: python
#
#        class SimpleComposer(Composer):
#            _lines = "{}\n{labeled}"
#
#        comp = SimpleComposer(1, labeled="one")
#        comp.compose()    # Renders "1\none"
#
#    Attributes:
#        _key_d0 (str): First template delimiter
#        _key_d1 (str): Second template delimiter
#        _key_n (str): N-length identifier
#        _key_nl (str): Newline joiner (N-length)
#        _key_bl (str): Newline joiner (1-length)
#        _key_dlen (int): Default template (line) length
#        _key_djin (str): Default template joiner
#    """
#    _key_d0 = ":"
#    _key_d1 = ","
#    _key_n = "n"
#    _key_nl = "\n"
#    _key_bl = " "
#    _key_dlen = 1
#    _key_djin = ""
#    composition = TypedProperty(Composition, "Template description")
#
#    def compose(self):
#        """
#        Compose the editor.
#
#        Automatically format the composer using the data objects. The formatter
#        works by iterating over the ``composition`` dataframe (a representation
#        of the template) building the strings to be used in formatting the
#        template. Positional arguments are taken from the special ``_args``
#        attribute without modification.
#
#        See Also:
#            The :attr:`~exa.core.composer.Composer.composition` provides
#            information about the template's parameters.
#        """
#        dct = vars(self)
#        kws = {}
#        # Dynamically identify available template composers
#        composers = self._get_composers()
#        # Iterate over the templates
#        for _, row in self.composition.iterrows():
#            name = row['name']    # Access using the property name
#            pname = "_" + name    # and non-property name
#            # If we don't have data to populate the template with...
#            if name not in dct and pname not in dct:
#                data = ""           # ...make it blank
#            else:                   # Otherwise retrieve and compose it
#                data = getattr(self, name)
#                typname = type(data).__name__
#                if typname in composers:
#                    data = composers[typname](data, **row.to_dict())
#                data = str(data)
#            kws[name] = data
#        return self.format(*self._args, **kws)
#
#    def format(self, *args, **kwargs):
#        """
#        Format the composer.
#
#        Args:
#            args (tuple): Positional formatter arguments
#            kwargs (dict): Keyword formatter arguments
#
#        Note:
#            Composers cannot be formatted 'inplace'; they always return a
#            new :class:`~exa.core.editor.Editor` object.
#
#        See Also:
#            Typically composers automatically format their templates using the
#            :func:`~exa.core.composer.Composer.compose` function.
#        """
#        text = self._preformat()
#        text = self._format(text, *args, **kwargs)
#        return self._postformat(text)
#
#    def copy(self):
#        """Return a copy of the current editor."""
#        special = ("_lines", "as_interned", "nprint", "meta", "encoding")
#        lines = self._lines[:]
#        as_interned = copy(self.as_interned)
#        nprint = copy(self.nprint)
#        meta = deepcopy(self.meta)
#        encoding = copy(self.encoding)
#        cp = {k: copy(v) for k, v in self._vars(True).items() if k not in special}
#        return Editor(lines, as_interned, nprint, meta, encoding, **cp)
#
#    def _preformat(self):
#        """
#        Generate the text representation of the current composer template.
#        Requires modification of the non-standard template strings
#        ('_exa_tmpl' format) to look like standard Python template strings.
#
#        .. code-block:: python
#
#            "{1:=:dct}"    # Special format template strings are converted
#            "{dct}"        # to standard format strings
#        """
#        text = str(self)
#        for tmpl in self.templates:
#            if self._key_d0 in tmpl:
#                text = text.replace(tmpl, tmpl.split(self._key_d0)[-1])
#        return text
#
#    @staticmethod
#    def _format(text, *args, **kwargs):
#        """
#        This function, by default, behaves similarly to the default editor's
#        format function but can be overwritten by subclasses if necessary. A
#        common example is when additional logic is needed depending
#        """
#        return text.format(*args, **kwargs)
#
#    def _postformat(self, text):
#        """
#        Called once formatting of the composer's template has completed and
#        determines whether to build a new editor or modify the current one.
#        """
#        cp = Editor(self.copy())
#        cp._lines = text.splitlines()
#        return cp
#
#    def _parse(self):
#        """Build the composition object which describes the template."""
#        # We need a parser for the template: the Composer editor's contents
#        # is a template to be formatted by default. Python objects such as
#        # lists and dicts (whatever is appropriate for the compositional task)
#        # are what store the data that populates the template.
#        lengths = []
#        joiners = []
#        names = []
#        types = []
#        for tmpl in self.templates:
#            try:
#                length, joiner, name = tmpl.split(self._key_d0)
#            except Exception:
#                name = tmpl
#                length = self._key_dlen
#                joiner = self._key_djin
#            try:
#                dtype = getattr(self.__class__.__class__, name)
#            except AttributeError:
#                dtype = None
#            lengths.append(length)
#            joiners.append(joiner)
#            names.append(name)
#            types.append(dtype)
#        dct = {'length': lengths, 'joiner': joiners, 'name': names, 'type': types}
#        self.composition = Composition.from_dict(dct)
#
#    def _get_composition(self):
#        """Lazy assignment of ``composition``."""
#        self.parse()
#
#    def _get_composers(self):
#        """
#        Helper function to identify ``_compose_\*`` functions.
#
#        By default, only str, dict, list, and tuples types have composition
#        functions: ``_compose_list``, etc. Additional keyword composition
#        functions can added (or existing ones can be modified).
#
#        .. code-block:: python
#
#            class MyComposer(Composer):
#                myvar = TypedProperty(str)
#
#                def _compose_str(self, value):
#                    # Put single quotes around the value and do nothing else
#                    return "'" + str(value) + "'"
#        """
#        composers = {}
#        for name in dir(self):
#            if name.startswith("_compose_"):
#                typ = name.split("_")[-1]
#                composers[typ] = getattr(self, name)
#        return composers
#
#    def _compose_ordereddict(self, val, **kwargs):
#        """Modify ordered dictionary keywords."""
#        return self._compose_dict(val, **kwargs)
#
#    def _compose_dict(self, val, **kwargs):
#        """Modify dictionary keywords."""
#        joiner = str(kwargs.pop("joiner", self._key_djin))
#        length = kwargs.pop("length", self._key_dlen)
#        lval = [str(k) + joiner + str(v) for k, v in val.items()]
#        if length == "n":
#            return self._key_nl.join(lval)
#        return self._key_bl.join(lval)
#
#    def _compose_list(self, val, **kwargs):
#        """Modify list keywords."""
#        joiner = str(kwargs.pop("joiner", self._key_djin))
#        return joiner.join(val)
#
#    def _compose_tuple(self, val, **kwargs):
#        """Modify tuple keywords."""
#        return self._compose_list(val, **kwargs)
#
#    def __init__(self, data=None, *args, **kwargs):
#        # Modify the first argument if a default template is provided
#        if hasattr(self, "_lines"):
#            if data is not None:
#                args = (data, ) + args
#            data = self._lines
#        elif isinstance(data, str) and not hasattr(self, "_lines") and "{" in data:
#            pass    # This is a check to make sure data is in fact a template
#        else:
#            raise TypeError("Missing ``data`` or ``_lines`` attribute.")
#        super(Composer, self).__init__(data, *args, **kwargs)
