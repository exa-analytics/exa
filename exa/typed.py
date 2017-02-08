# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Strongly Typed Abstract Base Classes
#####################################
Certain class objects within the Exa framework require static typing. These
classes often involve dynamically created methods that are dependent on
specific usage or implementation. The :class:`~exa.typed.Meta` object provides
a flexible metaclass that addresses these needs leveraging the built-in
`abc`_ framework.

.. code-block:: Python

    import six    # Convenient Python 2.7 compatibility

    class KlassMeta(Meta):
        attr1 = (int, float)
        attr2 = DataFrame

    class Klass(six.with_metaclass(KlassMeta, object)):
        def __init__(self, attr1, attr2):
            self.attr1 = attr1
            self.attr2 = attr2

In the above example, at runtime, the class definition "Klass" will be modified
such that 'attr1' is a property object whose setter checks to ensure that its
value is either an int or a float. Similarly, 'attr2' will become a property
whose setter checks to ensure that its value is a DataFrame. If a value is passed
for (for example) 'attr2' that can be converted to a DataFrame, automatic type
conversion will occur. More advanced uses are also possible:

.. code-block:: Python

    import six

    class KlassMeta(Meta):
        _getters = ("parse", )
        attr = DataFrame

    class Klass(six.with_metaclass(KlassMeta, object)):
        def parse_attr(self):
            # Perform some operation to obtain the value of attr
            self.attr = attr  # or 'return attr'

        def __init__(self, attr=None):
            self.attr = attr

By specifying the '_getters' attribute the statically typed property's getter
can be informed about what method to access if the value of the property has
not been set. This paradigm is sometimes called 'lazy evaluation'; the value
is only computed, parsed, etc. when it is requested (e.g. by calling
Klass().attr). Even more advanced usage is possible:

.. code-block:: Python

    import six

    class KlassMeta(Meta):
        _getters = ("parse", )
        _private = "private attribute"
        attr = DataFrame
        bttr = DataFrame

        def __new__(mcs, name, bases, clsdict):
            for name in ["attr", "bttr"]:
                f = simple_function_factory("parse_all", "parse", name)
                clsdict[f.__name__] = f
            clsdict['_private'] = mcs._private
            return super(KlassMeta, mcs).__new__(mcs, name, bases, clsdict)

    class Klass(six.with_metaclass(KlassMeta, object)):
        def parse_all(self):
            # Perform all parsing here or by calling other methods
            # Set all values here or in individually in other methods

        def __init__(self, attr=None):
            self.attr = attr

In this example, the metaclass (``KlassMeta``) utilizes the convenience
function, :func:`~exa.typed.simple_function_factory`, to generate methods
for the class (``Klass``) dynamically. This is useful when you have a single
method that typically does all of the work (e.g. ``Klass().parse_all``) but want
to be able to have the convenience of the previous example when calling specific
attributes (e.g. ``Klass().attr`` will call the dynamically generated method,
``Klass().parse_attr``, created by the :func:`~exa.typed.simple_function_factory`).
More complex function factories are possible. Finally, private attributes and
methods can also be defined by hand (i.e. ``clsdict['_private'] = ...``).

.. _abc: https://docs.python.org/3/library/abc.html
"""
from abc import ABCMeta
from exa.errors import TypeConversionError


def create_typed_attr(name, ptypes):
    """
    Create a property that enforces types.

    The minimal example shown below describes type enforcing. The properties
    created by this function have access to other functionality provided by
    Exa's abstract base class, :class:`~exa.typed.Meta`.

    .. code-block:: Python

        class Klass:
            @property
            def foo(self):
                return self._foo

            @foo.setter
            def foo(self, value):
                if isinstance(str):
                    self._foo = value

            @foo.deleter
            def foo(self):
                del self._foo

    Args:
        name (str): Name of strongly typed attribute
        ptypes (tuple): Immutable of valid types

    Returns:
        prop (property): Strongly typed property object

    See Also:
        See the module documentation for :mod:`~exa.typed`.
    """
    pname = '_' + name
    if not isinstance(ptypes, (tuple, list)):
        ptypes = (ptypes, )
    else:
        ptypes = tuple(ptypes)

    def getter(self):
        value = None
        # If not set or set to none, try to compute the value on-the-fly
        if not hasattr(self, pname) or getattr(self, pname) is None:
            for prefix in self._getters:
                cmd = "{}{}".format(prefix, pname)
                # Get the name of the compute function
                if hasattr(self, cmd):
                    value = getattr(self, cmd)()
                    # If the compute function returns a value
                    if value is not None:
                        # Set it
                        setattr(self, pname, value)
                        return value
                    break
            # If the attribute wasn't set or is still none, return none
            if not hasattr(self, pname) or getattr(self, pname) is None:
                return None
        return getattr(self, pname)

    def setter(self, obj):
        # Attempt to convert types
        if not isinstance(obj, ptypes):
            for ptype in ptypes:
                try:
                    obj = ptype(obj)
                    break
                except Exception:  # Many difference exceptions could be raised
                    pass
        # Allow setting as none or valid types
        if isinstance(obj, ptypes) or obj is None:
            setattr(self, pname, obj)
        else:
            raise TypeConversionError(obj, ptypes)

    def deleter(self):
        delattr(self, pname)    # Allows for dynamic attribute deletion

    return property(getter, setter, deleter)


def simple_function_factory(fname, prefix, attr):
    """
    Create a simple function of the following form:

    .. code-block: Python

        def prefix_attr(self):
            self.fname()

        f = simple_function_factory('parse_all', 'parse', 'section')
        # The function 'f' looks like:
        # def parse_section(self):
        #   self.parse_all()

    """
    def func(self, *args, **kwargs):
        getattr(self, fname)(*args, **kwargs)
    func.__name__ = "_".join((prefix, attr))
    return func


def yield_typed(obj):
    """
    Iterate over property names and type definitions.

    Args:
        obj: Class instance or definition

    Returns:
        iterator: List of (name, types) tuples
    """
    if not isinstance(obj, type):
        obj = obj.__class__
    mcs = obj.__class__
    for name, attr in vars(obj).items():
        if not name.startswith("_"):
            if isinstance(attr, property):
                yield (name, getattr(mcs, name))
            elif isinstance(attr, (tuple, list, type)):
                yield (name, attr)


class Meta(ABCMeta):
    """
    An abstract base class that supports strongly typed class attributes via
    properties and a host of other functionality. For examples and usage
    information see the module documentation, :mod:`~exa.typed`.
    """
    _getters = ()

    def __new__(mcs, name, bases, clsdict):
        # Strongly typed attributes
        for attr_name, types in yield_typed(mcs):
            clsdict[attr_name] = create_typed_attr(attr_name, types)
        # Methods
        clsdict['_getters'] = mcs._getters
        clsdict['_yield_typed'] = yield_typed
        return super(Meta, mcs).__new__(mcs, name, bases, clsdict)
