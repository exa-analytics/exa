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
        foo = (int, float)
        bar = DataFrame

    class Klass(six.with_metaclass(KlassMeta, object)):
        def __init__(self, foo=None, bar=None):
            self.foo = foo
            self.bar = bar

In the above example, at runtime, the class definition "Klass" will be modified
such that 'foo' is a property object whose setter checks to ensure that its
value is either an int or a float. Similarly, 'bar' will become a property
whose setter checks to ensure that its value is a DataFrame. If a value is passed
for (for example) 'bar' that can be converted to a DataFrame, automatic type
conversion will occur. More advanced uses are also possible.

.. code-block:: Python

    import six

    class KlassMeta(Meta):
        foo = DataFrame

    class Klass(six.with_metaclass(KlassMeta, object)):
        _getters = ("parse", )

        def parse_foo(self):
            # Perform some operation to obtain the value of attr
            self.foo = foo

        def __init__(self, foo=None):
            self.foo = foo

By specifying the '_getters' attribute the statically typed property's getter
can be informed about what method(s) to access if the value of the property has
not been set. This paradigm is sometimes called 'lazy evaluation'; the value
is only computed, parsed, etc. when it is requested (e.g. by calling
Klass().foo). Even more advanced usage is possible:

.. code-block:: Python

    import six

    class KlassMeta(Meta):
        foo = int
        bar = int
        _private = "'static' private attribute"

        def __new__(mcs, name, bases, clsdict):
            for name in ["attr", "bttr"]:
                f = simple_function_factory("parse_all", "parse", name)
                clsdict[f.__name__] = f
            clsdict['_private'] = mcs._private
            return super(KlassMeta, mcs).__new__(mcs, name, bases, clsdict)

    class Klass(six.with_metaclass(KlassMeta, object)):
        _getters = ("parse", )

        def parse_all(self):
            # Perform all parsing here or by calling other methods
            # Set all values here or in individually in other methods
            self.foo = 0
            self.bar = 1

        def __init__(self, foo=None, bar=None):
            self.foo = foo
            self.bar = bar

In this example, the metaclass (``KlassMeta``) utilizes the convenience
function, :func:`~exa.typed.simple_function_factory`, to generate methods
for the class (``Klass``) dynamically. This is useful when you have a single
method that typically does all of the work (e.g. ``Klass().parse_all``) and
prefer to have convenience methods generated dynamically (e.g. ``Klass().foo``
will call the dynamically generated method, ``Klass().parse_foo``, created by
the :func:`~exa.typed.simple_function_factory`). More complex function
factories are possible. Finally, pseudo static (private or not) attributes and
methods can also be defined by hand (i.e. ``clsdict['_private'] = baz`` where
``baz`` is the method or attribute in question).

.. _abc: https://docs.python.org/3/library/abc.html
"""
from abc import ABCMeta


def create_typed_attr(name, ptypes):
    """
    Create a property that enforces types.

    The minimal example shown below describes type enforcing. The properties
    created by this function have access to other functionality provided by
    Exa's abstract base class, :class:`~exa.typed.Meta` but do not depend
    on it.

    .. code-block:: Python

        class Klass:
            @property
            def foo(self):
                return self._foo

            @foo.setter
            def foo(self, value):
                if isinstance(value, ptypes):
                    self._foo = value

            @foo.deleter
            def foo(self):
                del self._foo

    Args:
        name (str): Name of strongly typed attribute
        ptypes (tuple): Iterable of valid types

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
        # If not set or set to none, try to compute the value on-the-fly
        if ((not hasattr(self, pname) or getattr(self, pname) is None)
            and hasattr(self, "_getters")):
            for prefix in self._getters:
                cmd = "{}{}".format(prefix, pname)
                # Get the name of the compute function
                if hasattr(self, cmd):
                    getattr(self, cmd)()    # Expect the function to set the value
                    break
            # If the attribute wasn't set or is still none, return none
            if not hasattr(self, pname) or getattr(self, pname) is None:
                return None
        return getattr(self, pname)

    def setter(self, obj):
        # Attempt to convert types
        if not isinstance(obj, ptypes) and obj is not None:
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
            raise TypeError("Cannot convert type {} to {}.".format(type(obj), ptypes))

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
    def __new__(mcs, name, bases, clsdict):
        # Strongly typed attributes
        for attr_name, types in yield_typed(mcs):
            clsdict[attr_name] = create_typed_attr(attr_name, types)
        # Other attributes and methods
        clsdict['_yield_typed'] = yield_typed
        return super(Meta, mcs).__new__(mcs, name, bases, clsdict)
