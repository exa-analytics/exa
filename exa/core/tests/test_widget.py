# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Notebook Widget Extensions
#############################################
"""
from unittest import TestCase
from traitlets import Unicode, Int
from exa.core.widget import Meta, DOMWidget, register


#@register                          # ipywidgets 7.x
@register("jupyter-exa.TestDOMWidget")    # ipywidgets 6.x
class TestDOMWidget(DOMWidget):
    """
    A test widget that displays text and tests bidirectional communication
    between Python and JavaScript.
    """
    _view_name = Unicode("TestDOMWidgetView").tag(sync=True)
    _model_name = Unicode("TestDOMWidgetModel").tag(sync=True)
    frontend_text = Unicode("Hello World!").tag(sync=True)
    backend_counter = Int(0).tag(sync=True)


class TestWidgets(TestCase):
    """
    Since command line unittests don't check for widget visibility, this test
    checks for roundtrip messages going from Python to JavaScript and back.
    """
    def test_domwidget(self):
        """Test comms."""
        w = TestDOMWidget()
        self.assertEqual(w.frontend_text, "Hello World!")
        self.assertEqual(w.backend_counter, 0)
        w.frontend_text = "changed"
        self.assertEqual(w.backend_counter, 1)

