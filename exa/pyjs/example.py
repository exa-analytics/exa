# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
"""
from ipywidgets import register, DOMWidget, Widget
from traitlets import Unicode, List


@register("hello.Hello")
class HelloWorld(DOMWidget):
    """Basic example."""
    _view_name = Unicode("HelloView").tag(sync=True)
    _model_name = Unicode("HelloModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)

    value = Unicode("Hello World!").tag(sync=True)


@register("example.Example")
class ExampleWidget(DOMWidget):
    """
    """
    _view_name = Unicode("ExampleView").tag(sync=True)
    _model_name = Unicode("ExampleModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)

    value = Unicode("Example text!").tag(sync=True)


@register("three.API")
class ThreeAPI(Widget):
    """
    """
    _view_name = Unicode("ThreeAPIView").tag(sync=True)
    _model_name = Unicode("ThreeAPIModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)

    api = List(["Geometry", "BufferGeometry"]).tag(sync=True)



@register("three.Renderer")
class Renderer(DOMWidget):
    """
    """
    _view_name = Unicode("RendererView").tag(sync=True)
    _model_name = Unicode("RendererModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)
