# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
API Builder
#########################
This module dynamically builds an API for available JavaScript libraries.
"""
import sys
from IPython.display import display
from ipywidgets import DOMWidget, Widget, widget_serialization
from traitlets import Unicode, Any
from exa.widgets import jsver, jsmod


class APIWidget(DOMWidget):
    """
    Template for dynamically generate API.
    """
    _view_module = Unicode(jsmod).tag(sync=True)
    _view_module_version = Unicode(jsver).tag(sync=True)
    _model_module = Unicode(jsmod).tag(sync=True)
    _model_module_version = Unicode(jsver).tag(sync=True)

    def __init__(self, *args, **kwargs):
        super(APIWidget, self).__init__()
        for i, arg in enumerate(args):
            setattr(self, self._order[i], arg)
        for name, attr in kwargs.items():
            setattr(self, name, attr)


def build_class(name, args):
    """
    """
    clsdict = {arg: Any(allow_none=True).tag(sync=True, **widget_serialization) for arg in args}
    clsdict['_view_name'] = Unicode(name + "View").tag(sync=True)
    clsdict['_model_name'] = Unicode(name + "Model").tag(sync=True)
    clsdict['_order'] = args
    clsdict['__doc__'] = "Args:\n    " + "\n    ".join(args)
    return type(name, (APIWidget, ), clsdict)


def build_api(modules):
    """
    Generate classes and modules.
    """
    for modname, attrs in modules.items():
        classes = {}
        for attrname, args in attrs.items():
            classes[attrname] = build_class(attrname, args)
        setattr(sys.modules['exa.widgets'], modname, type(modname, (object, ), classes))


class APIBuilder(Widget):
    """
    """
    _view_name = Unicode("APIBuilderView").tag(sync=True)
    _view_module = Unicode(jsmod).tag(sync=True)
    _view_module_version = Unicode(jsver).tag(sync=True)
    _model_name = Unicode("APIBuilderModel").tag(sync=True)
    _model_module = Unicode(jsmod).tag(sync=True)
    _model_module_version = Unicode(jsver).tag(sync=True)

    def _handle_custom_msg(self, content, buffers):
        """
        """
        if content['method'] == "build":
            build_api(content['content'])
        else:
            super(APIBuilder, self)._handle_custom_msg(content, buffers)


APIBuilder = APIBuilder()
display(APIBuilder)
