# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
from traitlets import Unicode
from ipywidgets import DOMWidget


jsver = "^0.4.0"
jsmod = "jupyter-exa"


class TestWidget(DOMWidget):
    _view_name = Unicode("TestWidgetView").tag(sync=True)
    _view_module = Unicode(jsmod).tag(sync=True)
    _view_module_version = Unicode(jsver).tag(sync=True)
    _model_name = Unicode("TestWidgetModel").tag(sync=True)
    _model_module = Unicode(jsmod).tag(sync=True)
    _model_module_version = Unicode(jsver).tag(sync=True)

    value = Unicode("Hello World!").tag(sync=True)
