# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
API Builder
#########################
This module provides the
"""
import six
from traitlets import Unicode
from ipywidgets import register
from exa.widgets.base import DOMWidget


@register("jupyter-exa.APIBuilder")
class APIBuilder(DOMWidget):
    """
    """
    _view_name = Unicode("APIBuilderView").tag(sync=True)
    _model_name = Unicode("APIBuilderModel").tag(sync=True)

    def build_api(self, *args, **kwargs):
        """
        """
        print("build api")
        print(args)
        print(kwargs)

    def __init__(self, *args, **kwargs):
        super(APIBuilder).__init__(*args, **kwargs)
        self.on_msg(self.build_api)
