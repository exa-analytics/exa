# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
import sys
from traitlets import Unicode, Any
from ipywidgets import DOMWidget, widget_serialization, Widget


tmp = None
jsver = "^0.4.0"
jsmod = "jupyter-exa"



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


def build_class(name, obj):
    clsdict = {arg: Any(allow_none=True).tag(sync=True, **widget_serialization) for arg in obj if not arg.startswith("__")}
    clsdict['_view_name'] = Unicode(name + "View").tag(sync=True)
    clsdict['_model_name'] = Unicode(name + "Model").tag(sync=True)
    clsdict['_order'] = obj
    clsdict['__doc__'] = "Args:\n    " + "\n    ".join(obj)
    return type(name, (APIWidget, ), clsdict)



def build_api(pkgs):
    """
    """
    for pkgname, api in pkgs.items():
        clses = {}     # Python classes to be created
        print(pkgname)
        for name, obj in api.items():
            clses[name] = build_class(name, obj)
        setattr(sys.modules['exa.apibuild'], pkgname, type(pkgname, (object, ), clses))


class TestWidget(Widget):
    _view_name = Unicode("TestWidgetView").tag(sync=True)
    _view_module = Unicode(jsmod).tag(sync=True)
    _view_module_version = Unicode(jsver).tag(sync=True)
    _model_name = Unicode("TestWidgetModel").tag(sync=True)
    _model_module = Unicode(jsmod).tag(sync=True)
    _model_module_version = Unicode(jsver).tag(sync=True)

    value = Unicode("Hello World!").tag(sync=True)

    def _handle_custom_msg(self, content, buffers):
        """
        """
        if content['method'] == "build":
            #tmp = content['content']
            build_api(content['content'])
        else:
            super(TestWidget, self)._handle_custom_msg(content, buffers)
