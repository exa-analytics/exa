# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Notebook Widget Extensions
#############################################
"""
from unittest import TestCase
from traitlets import Unicode
from exa.core.widget import Meta, Widget, register


#@register
class TestWidget(Widget):
    _view_name = Unicode("TestWidgetView").tag(sync=True)
    _model_name = Unicode("TestWidgetModel").tag(sync=True)
    value = Unicode("Hello World!").tag(sync=True)


class TestWidgets(TestCase):
    """
    """
    pass
