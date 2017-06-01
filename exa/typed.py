# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Typed Attribute Infrastructure
#####################################
This module provides a mechanism for dynamically creating typed class attributes
(via Python's property mechanism). These typed attributes enable higher level
class objects (such as :class:`~exa.core.container.Container`s) to have
systematic behavior for data processing and visualization. Additionally the
typed attributes of this module provide mechanisms for automatic 'getting' and
'setting', and other more complex machinery such as 'triggering' of other
functions on attribute changes.
"""
from abc import ABCMeta


class TypedAttribute(object):
    """
    A function-like class that creates typed class attributes that may have
    additional features.
    """
#    def __init__(self, types, docs, setter_finalize

    pass


def yield_typed(obj):
    """
    Iterate over property names and type definitions.

    Args:
        obj: Instance, class, or metaclass

    Returns:
        iterator: List of (name, types) tuples
    """
    if not isinstance(obj, type):
        obj = obj.__class__
    mcs = obj.__class__
    for name, attr in vars(mcs).items():
        if isinstance(attr, TypedAttribute):
            yield (name, attr)


class Typed(ABCMeta):
    """
    An abstract base class that supports strongly typed class attributes via
    properties and a host of other functionality.

    Certain class objects within the Exa framework require static typing. These
    classes often involve dynamically created methods that are dependent on
    specific usage or implementation. The :class:`~exa.typed.Typed` object provides
    a flexible metaclass that addresses these needs leveraging the abstract base
    class (`abc`_) framework.

    .. code-block:: python

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

    .. code-block:: python

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

    .. code-block:: python

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
        for attr_name, typedattr in yield_typed(mcs):
            clsdict[attr_name] = typedattr.create()
        return super(Typed, mcs).__new__(mcs, name, bases, clsdict)
