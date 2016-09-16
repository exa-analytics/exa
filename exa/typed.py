# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Strongly Typed Classes
####################################
This module provides the metaclass object :class:`~exa.typed.TypedMeta`. This
metaclass creates statically typed class attributes using the built-in property
mechanism. A usage example is given below:

.. code-block:: Python

    class Meta(TypedMeta):
        attr1 = (int, float)
        attr2 = DataFrame

    class Klass(metaclass=Meta):
        def __init__(self, attr1, attr2):
            self.attr1 = attr1
            self.attr2 = attr2

Under the covers, the :class:`~exa.typed.TypedMeta` (inherited) metaclass
creates a class object that looks like the following example. Additionally the
:class:`~exa.typed.TypedMeta` also provides a mechanism for automatic function
calls when a missing (but computable or parsable) attribute is requested.

.. code-block:: Python

    class Klass:
        # The following enforces the type of "attr1"
        @property
        def attr1(self):
            if self.
            return self._attr1

        @attr1.setter
        def attr1(self, obj):
            if not isinstance(obj, (int, float)):
                raise TypeError('attr1 must be int')
            self._attr1 = obj

        @property
        def attr2(self):
            ...
            ...

        def __init__(self, attr1, attr2):
            ...


.. code-block:: Python

    class Meta(TypedMeta)
"""


class TypedMeta(type):
    """
    A class for creating classes with enforced types. By convention this class
    also provies a mechanism for calling a computation (see
    :class:`~exa.analytics.container.Container`) or parsing (see
    :class:`~exa.management.editor.Editor`) function if the attribute requested
    does not exist.
    """
    @staticmethod
    def create_property(name, ptype):
        """
        Creates a custom property with a getter that performs computing
        functionality (if available) and raise a type error if setting
        with the wrong type.

        Note:
            By default, the setter attempts to convert the object to the
            correct type; a type error is raised if this fails.
        """
        pname = '_' + name
        def getter(self):
            # This will be where the data is store (e.g. self._name)
            # This is the default property "getter" for container data objects.
            # If the property value is None, this function will check for a
            # convenience method with the signature, self.compute_name() and call
            # it prior to returning the property value.
            if not hasattr(self, pname) and hasattr(self, '{}{}'.format(self._getter_prefix, pname)):
                self['{}{}'.format(self._getter_prefix, pname)]()
            if not hasattr(self, pname):
                raise AttributeError('Please compute or set {} first.'.format(name))
            return getattr(self, pname)

        def setter(self, obj):
            # This is the default property "setter" for container data objects.
            # Prior to setting a property value, this function checks that the
            # object's type is correct.
            if not isinstance(obj, ptype):
                try:
                    obj = ptype(obj)
                except Exception:
                    raise TypeError('Must be able to convert object {0} to {1} (or must be of type {1})'.format(name, ptype))
            setattr(self, pname, obj)

        def deleter(self):
            # Deletes the property's value.
            del self[pname]

        return property(getter, setter, deleter)

    def __new__(metacls, name, bases, clsdict):
        """
        Modification of the class definition occurs here; we iterate over all
        statically typed attributes and attach their property (see
        :func:`~exa.container.TypedMeta.create_property`) definition, returning
        the new class definition.
        """
        for k, v in vars(metacls).items():
            if isinstance(v, type) and k[0] != '_':
                clsdict[k] = metacls.create_property(k, v)
        return super().__new__(metacls, name, bases, clsdict)
