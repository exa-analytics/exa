# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Special Classes and Functions
#####################################
This module provides special class for supporting specific paradigms within the
Exa framework. The :class:`~exa.special.Singleton` provides the `singleton`_
programming paradigm. The :class:`~exa.special.Function` provides a class that
behaves like a function that can be used for lazy evaluation (among other
operations). The :class:`~exa.special.Typed` provides a metaclass for enforcing
strongly typed class attributes.

.. _singleton: https://en.wikipedia.org/wiki/Singleton_pattern
"""
from abc import ABCMeta


def create_typed_attr(name, ptypes):
    """
    Create a property that enforces types.

    The minimal example shown below describes type enforcing. The properties
    created by this function have access to other functionality provided by
    Exa's abstract base class, :class:`~exa.typed.Typed` but do not depend
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
class Singleton(type):
    """
    A metaclass that provides the `singleton`_ paradigm.

    Class objects that use this metaclass are limited to a single unique instance.
    A Python example of this is 'None'; all instances of None are references to
    the same object. This paradigm is useful when only a single instance of an
    object is necessary. The following is an example usage.

    .. code-block:: python

        import six    # For easy Python 2 compatibility

        class Highlander(six.with_metaclass(Singleton)):
            pass

    .. _singleton: https://en.wikipedia.org/wiki/Singleton_pattern
    """
    _singletons = {}

    def __call__(cls, *args, **kwargs):
        """
        Call on class definition creation; returns an already created class
        if one exists or creates a new one if it does not.
        """
        if cls not in cls._singletons:
            cls._singletons[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._singletons[cls]


class Function(object):
    """
    A class that behaves like a function.

    Although inheritable, this class works like a lazy evaluator.
    """
    pass


class Typed(ABCMeta):
    """
    An abstract base class that supports strongly typed class attributes via
    properties and a host of other functionality.

    Certain class objects within the Exa framework require static typing. These
    classes often involve dynamically created methods that are dependent on
    specific usage or implementation. The :class:`~exa.typed.Typed` object provides
    a flexible metaclass that addresses these needs leveraging the abstract base
    class (`abc`_) framework.

    .. code-block:: Python

        import six    # Convenient Python 2.7 compatibility

        class KlassTyped(Typed):
            foo = (int, float)
            bar = DataFrame

        class Klass(six.with_metaclass(KlassTyped, object)):
            def __init__(self, foo=None, bar=None):
                self.foo = foo
                self.bar = bar

    In the above example, at runtime, the class definition ``Klass`` will be
    modified such that ``foo`` is a property object whose setter checks to ensure
    that its value is either an int or a float. Similarly, ``bar`` will become a
    property whose setter checks to ensure that its value is a DataFrame. If a
    value is passed for (for example) ``bar`` that can be converted to a DataFrame,
    automatic type conversion will occur. More advanced uses are also possible.

    .. code-block:: Python

        import six

        class KlassTyped(Typed):
            foo = DataFrame

        class Klass(six.with_metaclass(KlassTyped, object)):
            _getters = ("parse", )

            def parse_foo(self):
                # Perform some operation to obtain the value of attr
                self.foo = foo

            def __init__(self, foo=None):
                self.foo = foo

    By specifying the ``_getters`` attribute, statically typed properties can be
    informed about what method(s) to access if their value has not (yet) been
    set. This is a form of lazy evaluation. Even more advanced usage is possible.

    .. code-block:: Python

        import six

        class KlassTyped(Typed):
            foo = int
            bar = int
            _private = "'static' private attribute"

            def __new__(mcs, name, bases, clsdict):
                for name in ["attr", "bttr"]:
                    f = simple_function_factory("parse_all", "parse", name)
                    clsdict[f.__name__] = f
                clsdict['_private'] = mcs._private
                return super(KlassTyped, mcs).__new__(mcs, name, bases, clsdict)

        class Klass(six.with_metaclass(KlassTyped, object)):
            _getters = ("parse", )

            def parse_all(self):
                # Perform all parsing here or by calling other methods
                # Set all values here or in individually in other methods
                self.foo = 0
                self.bar = 1

            def __init__(self, foo=None, bar=None):
                self.foo = foo
                self.bar = bar

    In this example, the metaclass (``KlassTyped``) utilizes the convenience
    function, :func:`~exa.special.simple_function_factory`, to generate methods
    for the class (``Klass``) dynamically. This is useful when you have a single
    method that typically does all of the work (e.g. ``Klass().parse_all``) and
    prefer to have convenience methods generated dynamically (e.g. ``Klass().foo``
    will call the dynamically generated method, ``Klass().parse_foo``, created by
    the :func:`~exa.special.simple_function_factory`). More complex function
    factories are possible. Finally, pseudo static (private or not) attributes and
    methods can also be defined by hand (i.e. ``clsdict['_private'] = baz`` where
    ``baz`` is the method or attribute in question).

    .. _abc: https://docs.python.org/3/library/abc.html
    """
    def __new__(mcs, name, bases, clsdict):
        # Strongly typed attributes
        for attr_name, types in yield_typed(mcs):
            clsdict[attr_name] = create_typed_attr(attr_name, types)
        # Other attributes and methods
        clsdict['_yield_typed'] = yield_typed
        return super(Typed, mcs).__new__(mcs, name, bases, clsdict)
