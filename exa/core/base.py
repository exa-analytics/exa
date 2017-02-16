# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Core Abstract Base Classes
#######################################
This module provides abstract base classes for analytical data objects
(:mod:`~exa.core.analytical`), discrete data objects (:mod:`~exa.core.data`),
editors (:mod:`~exa.core.editor`), and containers (:mod:`~exa.core.container`).
"""
import six
from uuid import UUID, uuid4
from abc import abstractmethod
from exa.typed import Meta


class ABCBaseMeta(Meta):
    """Strongly typed static attributes."""
    _getters = ('_get', )
    name = str
    meta = dict
    uid = UUID


class ABCBase(six.with_metaclass(ABCBaseMeta, object)):
    """
    Abstract base class for composite data representations such as the core
    :class:`~exa.core.editor.Editor` and :class:`~exa.core.container.Container`
    objects.
    """

    @abstractmethod
    def copy(self):
        """Must define a copy method."""
        pass

    def _get_uid(self):
        """Generate a new uid for this object."""
        self.uid = uuid4()

    def __init__(self, name=None, uid=None, meta=None, **kwargs):
        """Additional kwargs are grouped as a dictionary of metadata."""
        if meta is None and kwargs == {}:
            pass
        elif meta is None:
            meta = kwargs
        else:
            meta.update(kwargs)
        self.name = name
        self.uid = uid
        self.meta = meta
