# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Strongly Typed Classes
####################################
This module provides the metaclass object :class:`~exa.core.typed.TypedMeta`.
This metaclass creates statically typed class attributes using the built-in
property mechanism. A usage example is given below:

.. code-block:: Python

    class Meta(TypedMeta):
        attr1 = (int, float)
        attr2 = DataFrame

    class Klass(metaclass=Meta):
        _getter_prefix = "compute"
        def __init__(self, attr1, attr2):
            self.attr1 = attr1
            self.attr2 = attr2

Under the covers, the :class:`~exa.core.typed.TypedMeta` (inherited) metaclass
creates a class object that looks like the following example. Additionally the
:class:`~exa.core.typed.TypedMeta` also provides a mechanism for automatic
function calls when a missing (but computable or parsable) attribute is
requested.

.. code-block:: Python

    class Klass:
        @property
        def attr1(self):
            if not hasattr(self, attr1) and hasattr(self, 'compute_attr1'):
                self['compute_attr1']()
            if not hasattr(self, _attr1):
                raise AttributeError("Please compute or set attr1 first.")
            return getattr(self, "attr1")

        @attr1.setter
        def attr1(self, obj):
            if not isinstance(obj, (int, float)):
                raise TypeError('attr1 must be int')
            self._attr1 = obj

        ...

Strongly typed class attribtues helps exa containers and editors ensure correct
data object types are attached/created. This, in turn, ensures things such as
visualization and content management behave as expected.
"""
import warnings
from exa.core.errors import AutomaticConversionError


class TypedMeta(type):
    """
    A class for creating classes with enforced types. By convention this class
    also provies a mechanism for calling a computation (see
    :class:`~exa.core.container.Container`) or parsing (see
    :class:`~exa.core.editor.Editor`) function if the attribute requested
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
        if not isinstance(ptype, (tuple, list)):
            ptype = (ptype, )
        else:
            ptype = tuple(ptype)

        def getter(self):
            """
            This will be where the data is store (e.g. self._name)
            This is the default property "getter" for container data objects.
            If the property value is None, this function will check for a
            convenience method with the signature, self.[_getter_prefix]_name()
            and call it prior to returning the property value.
            """
            cmd = "{}{}".format(self._getter_prefix, pname)
            if (not hasattr(self, pname) or getattr(self, pname) is None) and hasattr(self, cmd):
                setattr(self, pname, getattr(self, cmd)())
            elif not hasattr(self, pname):
                return None
            return getattr(self, pname)

        def setter(self, obj):
            """
            This is the default property "setter" for container data objects.
            Prior to setting a property value, this function checks that the
            object's type is correct.
            """
            if obj is not None and not isinstance(obj, ptype):
                if len(ptype) == 1:
                    try:
                        obj = ptype[0](obj)
                        if isinstance(ptype[0], (tuple, list)):
                            warnings.warn("Please check automatic type conversion!")
                    except TypeError:
                        raise AutomaticConversionError(obj, ptype)
                else:
                    raise TypeError('Object "{}" must be of type(s) {} not {}.'.format(name, ptype, type(obj)))
            setattr(self, pname, obj)

        def deleter(self):
            del self[pname]

        return property(getter, setter, deleter)

    def __new__(mcs, name, bases, clsdict):
        """
        Modification of the class definition occurs here; we iterate over all
        statically typed attributes and attach their property (see
        :func:`~exa.typed.TypedMeta.create_property`) definition, returning
        the modified (i.e. property containing) class definition.
        """
        for k, v in vars(mcs).items():
            if isinstance(v, (type, tuple, list)):
                clsdict[k] = mcs.create_property(k, v)
        return super(TypedMeta, mcs).__new__(mcs, name, bases, clsdict)
