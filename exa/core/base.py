# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Base Class for Editors and Containers
#######################################
Abstract base class for :class:`~exa.core.editor.Editor` and
:class:`~exa.core.container.Container` objects.
"""
import six
from uuid import UUID, uuid4
from abc import abstractmethod
from exa.typed import Meta


class ABCBaseMeta(Meta):
    """Strongly typed static attributes."""
    _getters = ('_get', )
    name = str
    metadata = dict
    uid = UUID


class ABCBase(six.with_metaclass(Meta, object)):
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
        return uuid4()

    def __init__(self, name=None, uid=None, metadata=None, **kwargs):
        """Additional kwargs are grouped as a dictionary of metadata."""
        if metadata is None:
            metadata = kwargs
        else:
            metadata.update(kwargs)
        self.name = name
        self.uid = uid
        self.metadat = metadata
