# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Base JavaScript Widget
#########################
"""
import six
from traitlets import MetaHasTraits, Unicode, List, Dict
from ipywidgets import Widget as _Widget
from ipywidgets import DOMWidget as _DOMWidget
from ipywidgets import register
from exa.typed import TypedMeta
from exa.core.base import Base


jsver = "^0.4.0"
jsmod = "jupyter-exa"


class Meta(MetaHasTraits, TypedMeta):
    """A mixed metaclass for Exa widgets."""
    pass


#@register("hello.Hello")
class HelloWorld(six.with_metaclass(Meta, _DOMWidget, Base)):
    """
    """
    _view_name = Unicode("WidgetView").tag(sync=True)
    _view_module = Unicode(jsmod).tag(sync=True)
    _view_module_version = Unicode(jsver).tag(sync=True)
    _model_name = Unicode("WidgetModel").tag(sync=True)
    _model_module = Unicode(jsmod).tag(sync=True)
    _model_module_version = Unicode(jsver).tag(sync=True)
    value = "Hello World!"

    def info(self):
        pass


#@register("jupyter-exa.Widget")
#class Widget(six.with_metaclass(Meta, _Widget, Base)):
#    """Base Widget."""
#    _view_name = Unicode("WidgetView").tag(sync=True)
#    _view_module = Unicode(jsmod).tag(sync=True)
#    _view_module_version = Unicode(jsver).tag(sync=True)
#    _model_name = Unicode("WidgetModel").tag(sync=True)
#    _model_module = Unicode(jsmod).tag(sync=True)
#    _model_module_version = Unicode(jsver).tag(sync=True)
#
#    def info(self):
#        pass
#
#
##@register                             # ipywidgets 7.x
#@register("jupyter-exa.DOMWidget")    # ipywidgets 6.x
#class DOMWidget(six.with_metaclass(Meta, _DOMWidget, Base)):
#    """
#    Base DOMWidget
#    """
#    _view_name = Unicode("DOMWidgetView").tag(sync=True)
#    _model_name = Unicode("DOMWidgetModel").tag(sync=True)
#
#    def info(self):
#        """Display information about the widget parameters."""
#        pass
#
#
#
##class Builder(DOMWidget):
##    _view_name = Unicode("BuilderView").tag(sync=True)
##    _model_name = Unicode("BuilderModel").tag(sync=True)
##    extensions = List(trait=Unicode).tag(sync=True)
##    classes = Dict().tag(sync=True)
##    dynamic = Dict().tag(sync=True)
##
##    def __init__(self, *extensions, **kwargs):
##        super(Builder, self).__init__(**kwargs)
##        self.extensions = [str(item) for item in extensions]
##
##    def __init__(self, *args, **kwargs):
##        super(DOMWidget, self).__init__(*args, **kwargs)
##        self.on_msg(self.build_api)
#
#
##builder = Builder("three", "three-trackballcontrols")
##builder._ipython_display_()
