# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Wrapper for `ipywidgets`_
##########################

.. _ipywidgets: https://github.com/ipython/ipywidgets
"""
from ipywidgets import DOMWidget
from traitlets import Unicode


class HelloWorld(DOMWidget):
    _view_name = Unicode("HelloWorldView").tag(sync=True)
    _model_name = Unicode("HelloWorldModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("jupyter-exa").tag(sync=True)

    value = Unicode("Hello World").tag(sync=True)
