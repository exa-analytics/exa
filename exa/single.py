# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Singleton Metaclass
#####################################
This module provides :class:`~exa.single.Singleton`, a metaclass for coercing
a an arbitrary class object to support only a single instance of the class. The
canonical example in Python is 'None'. This is called the `singleton design pattern`_.
The following is an example usage.

.. code-block:: python

    import six    # For convenience

    class Highlander(six.with_metaclass(exa.single.Singleton)):
        pass

.. _singleton design pattern: https://en.wikipedia.org/wiki/Singleton_pattern
"""
class Singleton(type):
    """A metaclass for creating a singleton."""
    _singletons = {}

    def __call__(cls, *args, **kwargs):
        """
        Call on class definition creation; returns an already created class
        if one exists or creates a new one if it does not.
        """
        print("here2", cls, args, kwargs)
        if cls not in cls._singletons:
            print("here3")
            cls._singletons[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._singletons[cls]
