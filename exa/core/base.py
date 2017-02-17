# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Core Abstract Base Classes
#######################################
This module provides abstract base classes for all (built-in) data objects.
"""
import six
from uuid import UUID, uuid4
from abc import abstractmethod
from exa.typed import Meta


class ABCBaseMeta(Meta):
    """Strongly typed static attributes."""
    name = str
    meta = dict
    uid = UUID


class ABCBase(six.with_metaclass(ABCBaseMeta, object)):
    """
    Abstract base class for composite data representations such as the core
    :class:`~exa.core.editor.Editor` and :class:`~exa.core.container.Container`
    objects.
    """
    _getters = ('_get', )

    @abstractmethod
    def copy(self):
        """At a bare minimum a data object must define a copy method."""
        pass

    def _get_uid(self):
        """Generate a new uid for this object."""
        self.uid = uuid4()

    def __init__(self, name=None, uid=None, meta=None, **kwargs):
        """
        Base constructor for all data objects, editors, and containers.

        Args:
            name (str): Container name (optional)
            uid (UUID): Container uid (optional)
            meta (dict): Dictionary of metadata (optional)

        Note:
            Keyword arguments are added to this object's metadata.
        """
        if meta is None and kwargs == {}:
            pass
        elif meta is None:
            meta = kwargs
        else:
            meta.update(kwargs)
        self.name = name
        self.uid = uid
        self.meta = meta
