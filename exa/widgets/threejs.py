# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Wrapper for `three.js`_
##########################
For 3D visualization in the browser, `three.js`_ is an open source library that
provides the infrastructure necessary to render objects using (for example)
WebGL.

.. _three.js: https://threejs.org/
"""
from traitlets import Unicode
from .abcwidgets import ABCWidget


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
