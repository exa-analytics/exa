# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
API Builder
#########################
This module dynamically builds an API for available JavaScript libraries.
"""
from .base import Widget
from traitlets import Unicode


class APIBuilder(Widget):
    """
    """
    _view_name = Unicode("APIBuilderView").tag(sync=True)
    _model_name = Unicode("APIBuilderModel").tag(sync=True)

#    def build_api(self, *args, **kwargs):
#        """
#        """
#        print("build api")
#        print(args)
#        print(kwargs)
#
#    def __init__(self, *args, **kwargs):
#        super(APIBuilder).__init__(*args, **kwargs)
#        self.on_msg(self.build_api)
