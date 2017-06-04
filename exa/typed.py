# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Typed Attribute Infrastructure
#####################################
This module provides a mechanism for dynamically creating class properties
that enforce their attribute's type. The :func:`~exa.typed.cta`
function essentially creates a set of ``property`` related methods. The
following comparison can be made.

.. code-block:: Python

    class Klass:
        foo = cta("foo", ptypes)    # Where ptypes is a type or list of types

The above is the same as the following.

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

In addition to dynamically enforcing types using the ``property`` machinery of
Python, attributes created by :func:`~exa.typed.cta` enable
additional features such as lazy (automatic) assignment and triggering of other
method or function calls. Example usage can be found in the tests
(:mod:`~exa.tests.test_typed`).

See Also:
    :class:`~exa.core.base.Base`
"""
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
    for name, attr in vars(obj).items():
        if isinstance(attr, property) and "__typed__" in attr.__doc__:
            yield (name, attr)


def cta(name, ptypes, doc=None, setter_finalize=None):
    """
    Create a class attribute that enforces types and support lazy (automatic)
    assignment.

    This function can be used as part of the class definition similarly to the
    ``property`` function of the standard library.

    .. code-block:: python

        class Klass(object):
            typed = cta("typed", int, "an int")

            def __init__(self, typed=None):
                self.typed = typed

        inst = Klass("42")
        inst.typed           # Outputs integer 42

    Examples of more advanced usage can be found in :mod:`~exa.tests.test_typed`.

    Args:
        name (str): Variable name (used to build the property)
        ptypes (type, iterable): Type or list of types
        doc (str): Docstring
        setter_finalize (str, function): Function name or function to call after attribute is set

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
    doc = "__typed__" if doc is None else doc + "\n\n__typed__"
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
        setattr(self, pname, obj)
        # Finally call the setter_finalize method/function
        if isinstance(setter_finalize, str):
            getattr(self, setter_finalize)()
        elif callable(setter_finalize):
            try:
                setter_finalize()    # Assume static function (e.g. staticmethod)
            except TypeError:
                setter_finalize(self)    # Else class method
    # Provide a deleter for deletion of the actual data
    def deleter(self):
        delattr(self, pname)    # Allows for dynamic attribute deletion
    return property(getter, setter, deleter, doc=doc)
