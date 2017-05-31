# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Abstract Editors, Containers, and Data
#######################################
This module provides the base classes for editors, data objects, and containers.
Editors are responsible for parsing data in text files on disk into compact data
objects housed within containers. Containers provide a systematic API for
analysis and visualization of that data. Processing, analysis, and visualization
requires that the data structure (and types) are known; special data objects
allow for creation of such known structures/types that, in turn, enable a
cohesive processing API from the single entry object, the container.
The abstract class in this module provides some requirements for these objects.
"""
import six
from abc import abstractmethod, ABCMeta


class Base(six.with_metaclass(ABCMeta, object)):
    """
    Abstract base class for editors, data, and containers.

    Editors, (custom) data objects, and containers share some common API
    features that make operation with them systematic and easy to learn for
    users. For developers it provides a bare minimum requirements for extending
    the framework.

    Attributes:
        _getters (tuple): Default prefixes for automatic (lazy) function evalulation
        info (function): Display summary information about the current object
        _html_repr_ (function): Representation in the `Jupyter notebook`_

    See Also:
        :mod:`~exa.special`

    .. _Jupyter notebook: https://jupyter.org
    """
    _getters = ("compute", "parse", "_get")

    @abstractmethod
    def info(self):
        """
        The info function provides a description of the data/objects associated
        with the current object.
        """
        pass

    def _vars(self, include_underscore=False):
        """Helper to return dict items."""
        if include_underscore:
            return vars(self)
        else:
            return {k: v for k, v in vars(self).items() if not k.startswith("_")}

    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self._args = args
