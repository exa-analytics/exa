# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Typed Attribute Infrastructure
#####################################
This module provides a mechanism for dynamically creating typed class attributes
(via Python's property mechanism). These typed attributes enable higher level
class objects (such as :class:`~exa.core.container.Container`s) to have
systematic behavior for data processing and visualization. Additionally the
typed attributes of this module provide mechanisms for automatic 'getting' and
'setting', and other more complex machinery such as 'triggering' of other
functions on attribute changes.
"""
from abc import ABCMeta


class TypedAttribute(object):
    """
    A function-like class that creates typed class attributes that may have
    additional features.
    """
#    def __init__(self, types, docs, setter_finalize

    pass



