# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Wrapper for `three.js`_
##########################
For 3D visualization in the webbrowser, `three.js`_ is a library that provides
infrastructure to render objects using WebGL (among others). This module provides
and interface to `pythreejs`_ and extends its features specifc to the Exa framework.

.. _Jupyter notebook: https://jupyter-notebook.readthedocs.io/en/latest/
.. _three.js: https://threejs.org/
"""
from ipywidgets import Widget
from exa.app.abcwidgets import ABCWidget
from traitlets import Unicode, CFloat


class Renderer(ABCWidget):
    """
    Test0
    """
    _view_name = Unicode("RendererView").tag(sync=True)
    _model_name = Unicode("RendererModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)


class SubRenderer(Renderer):
    """
    Test1
    """
    _view_name = Unicode("SubRendererView").tag(sync=True)
    _model_name = Unicode("SubRendererModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)


class BaseWidget(Widget):
    """
    Base widget providing view/model module.
    """
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)
    _view_name = Unicode("BaseWidgetView").tag(sync=True)
    _model_name = Unicode("BaseWidgetModel").tag(sync=True)


class SphereGeometry(Widget):
    """
    Sphere Geometry.
    """
    _view_name = Unicode('SphereGeometryName').tag(sync=True)
    _model_name = Unicode('SphereGeometryModel').tag(sync=True)

    radius = CFloat(1).tag(sync=True)
