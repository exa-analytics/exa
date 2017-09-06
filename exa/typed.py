# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Strongly Typed Class Attributes
#####################################
This module provides a mechanism for enforcing class attribute types.
Knowing (and/or converting) variable types is useful for building high
performance workflows and algorithms. This feature is leveraged by
:class:`~exa.core.container.Container` objects for data organization,
analysis, and visualization.

.. code-block:: python

    class MyClass(Typed):
        myint = Typed(int, docs="Integer")

The :class:`~exa.typed.Typed` object is both a class and a callable. The above
class definition essentially creates the following class definition.

.. code-block:: python

    class MyClass(object):
        @property
        def myint(self):
            return self._myint

        @myint.setter
        def myint(self, value):
            if not isinstance(value, int):
                try:
                    value = int(value)
                except Exception as e:
                    raise TypeError("Cannot convert value") from e
            self._myint = value

Strongly typed attributes also provide a mechanism for triggering other
function calls (of the class to which they belong). Example usage can be found
in :mod:`~exa.tests.test_typed`.
"""
import six
from abc import ABCMeta


class Attr(object):
    """
    """
    pass


class Meta(ABCMeta):
    """
    Metaclass that parses a class definition and creates strongly
    typed attributes as properties on import.

    Args:
        flags (int):

    See Also:
        :class:`~exa.typed.Typed`
    """
    def __new__(mcs, name, bases, namespace, flags=None):
        for attr_name, attr in namespace.items():
            if isinstance(attr, TypedProperty):
                # Here we get the attribute name from the class definition
                # (in kwargs) and call the typed_property by calling
                # TypedProperty (which is a LazyFunction: calling a it
                # calls typed_property
                namespace[attr_name] = attr(name=attr_name)
        return super(TypedMeta, mcs).__new__(mcs, name, bases, namespace)


class Typed(six.with_metaclass(Meta, object)):
    """
    """
    pass


Attr = Attr()




def typed_property(name, ptypes, docs=None, sf=None, *args, **kwargs):
    """
    Create a class attribute that enforces types and support lazy (automatic)
    assignment.

    This function can be used as part of the class definition similarly to the
    ``property`` function of the standard library.

    .. code-block:: python

        class Klass(object):
            typed = typed_property("typed", int, "an int")

            def __init__(self, typed=None):
                self.typed = typed

        inst = Klass("42")
        inst.typed           # Outputs integer 42

    Examples of more advanced usage can be found in :mod:`~exa.tests.test_typed`.

    Args:
        name (str): Variable name (used to build the property)
        ptypes (type, iterable): Type or list of types
        docs (str): Docstring
        sf (str, function): Function name or function to call after attribute is set

    Note:
        Properties created by this function have the docstring containing "__typed__"
        to signify that this is not a 'normal' property object.

    See Also:
        See the module documentation for :mod:`~exa.typed`.
    """
    #if isinstance(ptypes, dict):

    if not isinstance(ptypes, (tuple, list)):
        ptypes = (ptypes, )
    else:
        ptypes = tuple(ptypes)
    docs = "__typed__" if docs is None else docs + "\n\n__typed__"
    # The private attribute is where the data content is actually stored
    pname = '_' + name
    # Property getter retrieves the private attribute that stores the data
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
    # The setter sets the private attribute with data
    def setter(self, obj):
        # Attempt to convert types
        if not isinstance(obj, ptypes) and obj is not None:
            for ptype in ptypes:
                try:
                    obj = ptype(obj)
                    break
                except Exception:  # Many different exceptions could be raised
                    pass
            else:
                raise TypeError("Cannot convert type {} to {}.".format(type(obj), ptypes))
        object.__setattr__(self, pname, obj)
        # Finally call the sf method/function
        if isinstance(sf, str):
            getattr(self, sf)()
        elif callable(sf):
            try:
                sf()    # Assume static function (e.g. staticmethod)
            except TypeError:
                sf(self)    # Else class method
    # Provide a deleter for deletion of the actual data
    def deleter(self):
        delattr(self, pname)    # Allows for dynamic attribute deletion
    return property(getter, setter, deleter, doc=docs)


class TypedProperty(LazyFunction):
    """
    Helper for creating typed attributes. Accepts the same arguments as
    :func:`~exa.typed.typed_property`. Example usage is as follows. For
    more typical usage see :class:`~exa.core.base.Base`.

    .. code-block:: python

        import six
        class Klass(six.with_metaclass(TypedMeta, object)):
            foo = TypedProperty(str, docs="foo attr")
            bar = TypedProperty(int, sf=lambda: print("bar set"))

    See Also:
        More common usage examples can be found in the docs related to
        :class:`~exa.typed.Typed` and :class:`~exa.core.base.Base`.
    """
    def __init__(self, ptypes, docs=None, sf=None):
        super(TypedProperty, self).__init__(fn=typed_property, ptypes=ptypes, sf=sf, docs=docs)


class TypedMeta(ABCMeta):
    """
    Metaclass for preparing strongly typed property attributes.
    Properties are attached to class definitions; this metaclass automatically
    creates type enforcing properties (see :func:`~exa.typed.typed_property`)
    for all class attributes defined as follows. Typical usage is through
    either the :class:`~exa.typed.Typed` object or :class:`~exa.core.base.Base`.

    .. code-block:: python

        import six   # Python 2 compatibility
        class Klass(six.with_metaclass(TypedMeta, bases)):
            attr = TypedProperty(*args, **kwargs)
    """
    def __new__(mcs, name, bases, namespace):
        for attr_name, attr in namespace.items():
            if isinstance(attr, TypedProperty):
                # Here we get the attribute name from the class definition
                # (in kwargs) and call the typed_property by calling
                # TypedProperty (which is a LazyFunction: calling a it
                # calls typed_property
                namespace[attr_name] = attr(name=attr_name)
        return super(TypedMeta, mcs).__new__(mcs, name, bases, namespace)


class Typed(six.with_metaclass(TypedMeta, object)):
    """
    A concrete base class that supports strongly attributes, used when
    subclassing ``object`` is all that is needed (as the base).

    .. code-block:: python

        class Klass(Typed):
            foo = TypedProperty(dict)

    The above is functionally the same (but shorter) than the following,
    more explicit, code.

    .. code-block:: python

        import six
        class Klass(six.with_metaclass(TypedMeta, object)):
            foo = TypedProperty(dict)
    """
    pass


def yield_typed(obj):
    """
    Iterate over property names and type definitions.

    Strongly typed properties are distinguished from standard property
    objects by the inclusion of the string '__typed__' in the ``__doc__``
    attribute of the (property) object.

    Args:
        obj: Instance of a class or the class itself.

    Returns:
        iterator: List of (name, types) tuples
    """
    if not isinstance(obj, type):
        obj = obj.__class__
    for name in dir(obj):
        attr = getattr(obj, name)
        if isinstance(attr, property) and "__typed__" in attr.__doc__:
            yield (name, attr)


