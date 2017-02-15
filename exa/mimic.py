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
generated (and updated) dynamically based on the ``_obj`` attributed.

Warning:
    Methods of mimicked objects that create new objects return mimicked objects.
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

        # Iterate over all attributes/methods of the object (omitting native)
        for name in set(dir(self._obj)).difference(dir(self)):
            value = getattr(self._obj, name)
            if callable(value):
                attr = callable_helper(name)
            else:
                attr = attribute_helper(name)
            setattr(self, name, attr)

    def __getitem__(self, name):
        ret = self._obj.__getitem__(name)
        self._update_api()
        return Mimic(ret)

    def __setitem__(self, name, value):
        self._obj.__setitem__(name, value)
        self._update_api()

    def __delitem__(self, name):
        self._obj.__delitem__(name)
        self._update_api()

    def __init__(self, obj):
        self._obj = obj
        self._update_api()

    def __repr__(self):
        return "Mimic({})".format(repr(self._obj))
