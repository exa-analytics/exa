# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""

Base JavaScript Widget
#########################
"""
import six
from traitlets import MetaHasTraits, Unicode, List, Dict
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

    def build_api(self, widget):
        pass

    def __init__(self, *args, **kwargs):
        super(DOMWidget, self).__init__(*args, **kwargs)
        self.on_msg(self.build_api)


class Builder(DOMWidget):
    _view_name = Unicode("BuilderView").tag(sync=True)
    _model_name = Unicode("BuilderModel").tag(sync=True)
    extensions = List(trait=Unicode).tag(sync=True)
    classes = Dict().tag(sync=True)
    dynamic = Dict().tag(sync=True)

    def __init__(self, *extensions, **kwargs):
        super(Builder, self).__init__(**kwargs)
        self.extensions = [str(item) for item in extensions]


builder = Builder("three", "three-trackballcontrols")
builder._ipython_display_()
