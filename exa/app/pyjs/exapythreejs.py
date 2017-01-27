# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Wrapper for `pythreejs`_
##########################
For 3D visualization in the webbrowser, `three.js`_ is a library that provides
infrastructure to render objects using WebGL (among others). The `pythreejs`_
project is a python wrapper around `three.js`_ intended to be built upon for
creating custom 3D widgets for the `Jupyter notebook`_. This module provides
and interface to `pythreejs`_ and extends its features specifc to the Exa
framework.

.. _pythreejs: https://github.com/jovyan/pythreejs
.. _Jupyter notebook: https://jupyter-notebook.readthedocs.io/en/latest/
.. _three.js: https://threejs.org/
"""
import pythreejs as py3js
from ipywidgets import register
from traitlets import Unicode


class Renderer(py3js.Renderer):
    """Custom Renderer (an instance of a widget) for the Exa framework."""
    _view_name = Unicode("RendererView").tag(sync=True)
    _model_name = Unicode("RendererModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)



#class Scene(py3js.Scene):
#    """Custom Scene (an instance of a widget) for the Exa framework."""
#    _view_name = Unicode("SceneView").tag(sync=True)
#    _model_name = Unicode("SceneModel").tag(sync=True)
#    _view_module = Unicode("jupyter-exa").tag(sync=True)
#    _model_module = Unicode("jupyter-exa").tag(sync=True)

