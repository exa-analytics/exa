# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Mimicked Objects
#####################################
In certain contexts it can be advantageous to mimic the behavior of an object
instead of inheriting its attributes, properties, and methods via sub-classing.
Instead of using inheritance,

.. code-block:: python

    class MyClass(OtherClass):
        def...
        attr...
        prop...

where def..., attr..., and prop.. are methods, attributes, and properties,
which are typed 'by hand', a mimicked class takes the following approach.

.. code-block:: python

    class Mimic(object):
        def __init__(self, obj):
            self._obj = obj

        def...
        attr...
        prop...

Where methods, attributes, and properties (def..., attr..., and prop...) are
generated (and updated) dynamically based on the ``_obj`` attributed. To modify
objects of the :class:`~exa.mimic.Mimic` itself, use the following syntax.

.. code-block:: python

    mimic = Mimic(myobj)
    object.__getattr__(mimic, "name")    # Get attribute
    object.__setattr__(mimic, "name")    # Set attribute
    object.__delattr__(mimic, "name")    # Delete attribute

Warning:
    Methods of mimicked objects that create new objects return mimicked objects.
    Mimicking None is not supported.
"""
class Mimic(object):
    """A class that behaves indentically to another object."""
    def _update_api(self):
        """Update the mimicked API to match its target object."""
        # First define a couple of helper functions for building the API
        def callable_helper(name):
            """Helper function for callable API."""
            f = getattr(self._obj, name)
            def func(*args, **kwargs):
                """Callable wrapper."""
                ret = f(*args, **kwargs)
                self._update_api()
                return Mimic(ret)
            func.__name__ = f.__name__
            func.__doc__ = f.__doc__
            return func

        def attribute_helper(name):
            """Helper function for attributes/properties API."""
            def getter():
                ret = getattr(self._obj, name)
                self._update_api()
                return Mimic(ret)
            return getter

        # Delete any previously attached methods
        for name in self._methods:
            object.__delattr__(self, name)
        # Iterate over all attributes/methods of the object (omitting native)
        for name in set(dir(self._obj)).difference(dir(self)):
            value = getattr(self._obj, name)
            if callable(value):
                attr = callable_helper(name)
            else:
                attr = attribute_helper(name)
            object.__setattr__(self, name, attr)
            self._methods.append(name)

    def __getitem__(self, name):
        ret = self._obj.__getitem__(name)
        self._update_api()
        return ret

    def __setitem__(self, name, value):
        self._obj.__setitem__(name, value)
        self._update_api()

    def __delitem__(self, name):
        self._obj.__delitem__(name)
        self._update_api()

    def __getattr__(self, name):
        ret = getattr(self._obj, name)
        self._update_api()
        return ret

    def __setattr__(self, name, value):
        setattr(self._obj, name, value)
        self._update_api()

    def __delattr__(self, name):
        delattr(self._obj, name)
        self._update_api()

    def __format__(self, *args, **kwargs):
        self._obj.__format__(*args, **kwargs)

    def __eq__(self, other):
        try:
            return self._obj.__eq__(other)
        except AttributeError:
            return self._obj.__cmp__(other)

    def __ge__(self, other):
        return self._obj.__ge__(other)

    def __gt__(self, other):
        return self._obj.__gt__(other)

    def __le__(self, other):
        return self._obj.__le__(other)

    def __lt__(self, other):
        return self._obj.__lt__(other)

    def __ne__(self, other):
        return self._obj.__ne__(other)

    def __hash__(self):
        return self._obj.__hash__()

    def __reduce__(self, *args, **kwargs):
        return self._obj.__reduce__(*args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        return self._obj.__reduce_ex__(*args, **kwargs)

    def __sizeof__(self):
        return self._obj.__sizeof__()

    def __len__(self):
        return self._obj.__len__()

    def __str__(self):
        return self._obj.__str__()

    def __repr__(self):
        return repr(self._obj)

    @property
    def __class__(self):
        return self._obj.__class__

    def __init__(self, obj):
        # Use this syntax because we want to set the attribute on
        # this object rather than on self._obj (see setattr method).
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_methods", [])
        self._update_api()

