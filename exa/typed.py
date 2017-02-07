# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Strongly Typed Metaclass
####################################
Certain class objects within the Exa framework require static typing. Additionally,
these classes often involve abstract methods that are dependent on the specific
subclassing to be done. This module provides a type enforcing abstract base
class (metaclass). Static typing is accomplished via property objects.

.. code-block:: Python

    import six

    class KlassMeta(Meta):
        _getters = ("compute", )
        attr1 = (int, float)
        attr2 = DataFrame

    class Klass(six.with_metaclass(KlassMeta, object)):
        def compute_attr1(self):
            self.attr1 = 1.0

        def __init__(self, attr1, attr2):
            self.attr1 = attr1
            self.attr2 = attr2

At runtime, the class object, "Klass", creates property attributes "attr1" and
"attr2" (stored as "_attr1" and "_attr2"). The property setter performs all of
the type checking. The property getter can attempt to parse or compute the
attribute (via the "_getters" attribute). In the example above, "_getters" is
a tuple with only the "compute" prefix listed. If "attr1" were not set, any
attempt to get this attribute would first make a call to the "compute_attr1"
function.
"""
from abc import ABCMeta
from exa.errors import AutomaticConversionError


def create_typed_attr(name, ptypes):
    """
    Create a property that enforces types. Akin to:

    .. code-block:

    Args:
        name (str): Name of strongly typed attribute
        ptypes (tuple): Immutable of valid types

    Returns:
        prop (property): Strongly typed property object

    See Also:
        :mod:`~exa.typed` documentation
    """
    pname = '_' + name
    if not isinstance(ptypes, (tuple, list)):
        ptypes = (ptypes, )
    else:
        ptypes = tuple(ptypes)

    def getter(self):
        """Attempt to compute/parse/etc the attribute and return it."""
        fmt = "{}{}".format
        try:
            return getattr(self, pname)
        except AttributeError:
            for prefix in self._getters:
                cmd = fmt(prefix, pname)
                if hasattr(self, cmd):
                    getattr(self, cmd)()    # Call the compute/parse/etc function
                    if hasattr(self, pname):  # In case of multiple functions
                        break
        if hasattr(self, pname):
            return getattr(self, pname)

    def setter(self, obj):
        """Check the type, attempt to convert if necessary, and set it."""
        if not isinstance(obj, ptypes):
            for ptype in ptypes:
                try:
                    obj = ptype(obj)
                    break
                except Exception:
                    pass
        if isinstance(obj, ptypes) or obj is None:
            setattr(self, pname, obj)
        else:
            raise AutomaticConversionError(obj, ptypes)

    def deleter(self):
        """Property deleter."""
        del self.__dict__[pname]

    return property(getter, setter, deleter)


def simple_function_factory(fname, prefix, attr):
    """
    Create a simple function of the following form:

    .. code-block: Python

        def prefix_attr(self):
            self.fname()

        # Running
        simple_function_factory('parse_all', 'parse', 'section')
        # Returns
        def parse_section(self):
            self.parse_all()

    """
    def func(self, *args, **kwargs):
        getattr(self, fname)(*args, **kwargs)
    func.__name__ = "_".join((prefix, attr))
    return func


def get_properties(clsobj):
    """Get a list of property attribute names and types."""
    props = []
    for name, attr in vars(clsobj.__class__).items():
        if isinstance(attr, property):
            props.append((name, getattr(clsobj.__class__.__class__, name).__name__))
    return props


class Meta(ABCMeta):
    """
    An abstract base class that supports strongly typed class attributes via
    property objects.

    See Also:
        :func:`~exa.typed.create_typed_attr`
    """
    _getters = ()

    def __new__(mcs, name, bases, clsdict):
        """
        At runtime the class definition is modified; all public variables are
        converted into typed attributes.
        """
        # Strongly typed attributes
        for name, definition in vars(mcs).items():
            if not name.startswith("_") and isinstance(definition, (type, tuple, list)):
                clsdict[name] = create_typed_attr(name, definition)
        # Methods
        clsdict["_properties"] = get_properties
        clsdict["_getters"] = mcs._getters
        return super(Meta, mcs).__new__(mcs, name, bases, clsdict)
