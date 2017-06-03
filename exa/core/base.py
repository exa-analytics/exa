# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Abstract Base Class for Core Objects
#######################################
This module provides a standard base class for all core objects. Core objects
are required to have an implementation of the :func:`~exa.core.base.Base.info`
method. Additionally, the base class accepts and stores all positional and
keyword arguments that reach its ``init`` method. Positional arguments are
stored in the ``_args`` keyword while keyword arguments are attached directly
to the class instance (by their name).
"""
import six
from abc import abstractmethod, ABCMeta


class BaseMeta(ABCMeta):
    """Used for Python 2 compatibility."""
    pass


class Base(six.with_metaclass(BaseMeta, object)):
    """
    Abstract base class for editors, data, and containers.

    The base class requires a concrete implementation of the ``info`` method,
    which is used to provide a summary of the object in question. The
    ``_getters`` attribute is used in concert with features to :mod:`~exa.typed`
    to enforce class attribute types and support lazy evaluation.

    Attributes:
        _getters (tuple): Default prefixes for automatic (lazy) function evaluation

    See Also:
        :mod:`~exa.typed`
    """
    _getters = ("compute", "parse", "_get")

    @abstractmethod
    def info(self):
        """
        The info function provides a summary of the data or objects
        contained in the current instance.
        """
        pass

    def _vars(self, include_underscore=False):
        """
        A ``vars`` like method that optionally does not include attributes
        that start with a leading underscore.
        """
        if include_underscore:
            return vars(self)
        else:
            return {k: v for k, v in vars(self).items() if not k.startswith("_")}

    def __init__(self, *args, **kwargs):
        """
        Positional arguments are set to the ``_args`` attribute; keyword
        arguments are attached by their names.
        """
        self._args = args
        for name, value in kwargs.items():
            setattr(self, name, value)
