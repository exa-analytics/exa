# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Composer Editors
####################################
Composers are editor like objects that are used to programmatically create
text files using a standard structure of template. This is akin to, for example,
JSON; the JSON library does not know a priori what data it will contain only
how to format whatever data it receives. Similarly, composers can be built
using a standard format or a template and have their data fields/values be
populated dynamically.
"""
import six
from abc import ABC, abstractmethod
from exa.special import Typed
from .editor import Editor


class ComposerMeta(Typed):
    """
    """
    _template = None
    _join = None
    _delim = None
    _sep = None



class Composer(six.with_metaclass(ComposerMeta, ABC)):
    """
    """

    @classmethod
    def from_string(cls, text):
        """
        """

        pass

    @classmethod
    def from_editor(cls, editor):
        """Build a composer from an editor."""
        return cls.from_string(str(editor))

    def to_editor(self):
        """
        """
        return Editor(self.format())

    def format(self):
        """
        """
        pass

    @abstractmethod
    def _formatter(self):
        """
        The formatter builds the
        """
        pass
