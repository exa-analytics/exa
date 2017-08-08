# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Test Base Widgets
#############################################
"""
import os, platform
from traitlets import Unicode
from unittest import TestCase
from subprocess import check_output
from exa.widgets.base import Widget, DOMWidget


nbname = "test_base.ipynb"
cwd = os.path.dirname(os.path.abspath(__file__))
nbpath = os.path.join(cwd, nbname)
tmppath = os.path.join(cwd, "test_base.ipynb.output")
htmlpath = os.path.join(cwd, nbname.replace(".ipynb", ".html"))
prckws = {'shell': True} if platform.system().lower() == "windows" else {}


class WidgetTest(Widget):
    """
    """
    _view_name = Unicode("WidgetTestView").tag(sync=True)
    _model_name = Unicode("WidgetTestModel").tag(sync=True)
    value = Unicode("WidgetTest value").tag(sync=True)

    def _handle_custom_msg(self, *args, **kwargs):
        """
        """
        self.value_response = args[0]

    def __init__(self, *args, **kwargs):
        super(WidgetTest, self).__init__(*args, **kwargs)
        self.value_response = ""


class DOMWidgetTest(DOMWidget):
    """
    """
    _view_name = Unicode("DOMWidgetTestView").tag(sync=True)
    _model_name = Unicode("DOMWidgetTestModel").tag(sync=True)
    value = Unicode("DOMWidgetTest value").tag(sync=True)


class TestWidgets(TestCase):
    """
    """
    def setUp(self):
        """
        """
        ret = check_output(["jupyter", "nbconvert", "--exec",
                            "--ExecutePreprocessor.kernel_name=python", nbpath],
                           cwd=cwd, **prckws)
        print(ret)
        self.expected = ["WidgetTest value", "DOMWidgetTest value", "test", "test"]
        self.expected_dom = self.expected[:]
        self.expected_dom[0] = ""

    def test_value_check(self):
        """
        """
        try:
            with open(tmppath) as f:
                result = [line.strip() for line in f.readlines()]
            check = result == self.expected
            if check == False:
                check = result == self.expected_dom
            self.assertTrue(check)
        except Exception as e:
            self.fail(msg=str(e))

    def tearDown(self):
        """
        """
        try:
            os.remove(tmppath)
            os.remove(htmlpath)
        except Exception as e:
            self.fail(msg=str(e))
