# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Abstract Base Widgets
##########################
For 3D visualization in the webbrowser, `three.js`_ is a library that provides
infrastructure to render objects using WebGL (among others). This module provides
and interface to `pythreejs`_ and extends its features specifc to the Exa framework.

.. _Jupyter notebook: https://jupyter-notebook.readthedocs.io/en/latest/
.. _three.js: https://threejs.org/
"""
from ipywidgets import DOMWidget
from traitlets import Unicode


class ABCWidget(DOMWidget):
    """Abstract base widget."""
    _view_name = Unicode("ABCView").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_name = Unicode("ABCModel").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)

