# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Abstract Base Widgets
##########################
"""
from traitlets import Unicode
from ipywidgets import DOMWidget


class ABCWidget(DOMWidget):
    """Abstract base widget."""
    _view_name = Unicode("ABCView").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_name = Unicode("ABCModel").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)

