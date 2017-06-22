# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""

Base JavaScript Widget
#########################
"""
import six
from traitlets import MetaHasTraits, Unicode
from ipywidgets import DOMWidget as _DOMWidget
from ipywidgets import register
from exa.typed import TypedMeta
from exa.core.base import Base


class Meta(MetaHasTraits, TypedMeta):
    """A mixed metaclass for Exa widgets."""
    pass


#@register                          # ipywidgets 7.x
@register("jupyter-exa.DOMWidget")    # ipywidgets 6.x
class DOMWidget(six.with_metaclass(Meta, _DOMWidget, Base)):
    """
    Base DOMWidget
    """
    _view_name = Unicode("DOMWidgetView").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _view_module_version = Unicode("^0.4.0").tag(sync=True)    # Matches js/package.json
    _model_name = Unicode("DOMWidgetModel").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module_version = Unicode("^0.4.0").tag(sync=True)   # Matches js/package.json

    def info(self):
        """Display information about the widget parameters."""
        pass
