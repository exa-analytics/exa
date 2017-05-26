# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Singleton and Related Design Patterns
#######################################
The `singleton`_ design pattern can be useful when only one instance of a given
object is required. This module provides both an inheritable singleton metaclass
as well as a singleton factory class.

.. _singleton: https://en.wikipedia.org/wiki/Singleton_pattern
"""


class SharedState(object):
    """
    An object that shares one (global) state for all of its instances.

    This design pattern allows the creation of any number of instances of the
    class, all of which share the same state (``__dict__``).

    .. code-block:: python

        class Shared(SharedState):
            def __init__(self, value):
                self.value = value

        obj0 = Shared(1)
        obj0.value     # 1
        obj1 = Shared(42)
        obj0.value     # 42
        obj1.value     # 42
        obj0 is obj1   # False
        obj0.value is obj1.value    # True

    Note:
        This is sometimes called the Borg design pattern
    """
    __shared_state = {}

    def __new__(cls, *args, **kwargs):
        inst = super(SharedState, cls).__new__(cls)
        inst.__dict__ = cls.__shared_state
        return inst


class Singleton(type):
    """
    A metaclass that enforces the `singleton`_ design pattern.

    A class object (i.e. class definition) is an instance of a metaclass. The
    singleton pattern is enforced by having this (meta)class create only a single
    class (definition) object.

    .. code-block:: python

        import six    # Python 2/3 compatibility

        class Highlander(six.with_metaclass(Singleton)):
            pass

        obj0 = Highlander()
        obj1 = Highlander()
        assert obj0 is obj1
        assert id(obj0) == id(obj1)

    Tip:
        A singleton factory can be creatd by inheriting this object.

    .. _singleton: https://en.wikipedia.org/wiki/Singleton_pattern
    """
    _class_objects = {}    # Stores class objects (class definitions)

    def __call__(cls, *args, **kwargs):
        """
        If a given class has not yet been created, create it.
        Otherwise return an existing class object (class definition).
        """
        print("single call")
        if cls not in cls._class_objects:
            cls._class_objects[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._class_objects[cls]
