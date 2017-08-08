# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for JavaScript Widget Extensions
#############################################
In the Jupyter notebook environment, JavaScript extensions can be used to
create interactive, browser-based, extensions to Python objects. These
can be used to, for example, provide 3D visualizations. In order to test
these features this module executes a Jupyter notebook file and checks the
output written as part of running the notebook.

This module also tests the possibility of combining
:class:`~exa.core.container.Container` and :class:`~exa.core.widget.DOMWidget`.
Combined, these classes can create a data container that has an interactive
JavaScript representation rather than a static HTML/text representation.
"""
#import os
#import platform
##from unittest import TestCase
#from traitlets import Unicode, List, Int, Bool
##from subprocess import check_call
##from exa.core.container import Container
#from exa.widgets.base import DOMWidget
#
#
#prckws = {'shell': True} if platform.system().lower() == "windows" else {}
#nbname = "test_widget.ipynb"
#cwd = os.path.dirname(os.path.abspath(__file__))
#nbpath = os.path.join(cwd, nbname)
#tmppath = os.path.join(cwd, "test_widget.ipynb.output")
#htmlpath = os.path.join(cwd, nbname.replace(".ipynb", ".html"))
#
#from functools import wraps
#def yield_for_change(widget, attribute):
#    """
#    Pause a generator to wait for a widget change event.
#
#    This is a decorator for a generator function which pauses the generator on yield
#    until the given widget attribute changes. The new value of the attribute is
#    sent to the generator and is the value of the yield.
#    """
#    def f(iterator):
#        @wraps(iterator)
#        def inner():
#            print(iterator)
#            i = iterator()
#            def next_i(change):
#                try:
#                    print("changing", change)
#                    i.send(change.new)
#                except StopIteration as e:
#                    print("stopping")
#                    print(str(e))
#                    print("unobs")
#                    widget.unobserve(next_i, attribute)
#            widget.observe(next_i, attribute)
#            # start the generator
#            next(i)
#        return inner
#    return f
#
#
#class TestMSG(DOMWidget):
#    _view_name = Unicode("TestMSGView").tag(sync=True)
#    _model_name = Unicode("TestMSGModel").tag(sync=True)
#    switch = Bool(False).tag(sync=True)
#    telephone = Int(0).tag(sync=True)
#
#    def _handle_custom_msg(self, *args, **kwargs):
#        print("msg received")
#        print(args)
#        print(kwargs)
#
#    def __init__(self, *args, **kwargs):
#        super(TestMSG, self).__init__(*args, **kwargs)
#        builder(self)
#
#
#def builder(obj):
#    @yield_for_change(obj, "telephone")
#    def watcher():
#        while True:
#        #for i in range(5):
#            print("telephone updated observed")
#            yield
#            #x = yield
#            #print("continue with value {}".format(x))
#    watcher()
#
#
#
#
#
##expected = ["('Hello World!', 0)",
##            "('Hello', 1)",
##            "('Hello World!', 0)",
##            "('Hello', 1)"]
#
#
##@register                          # ipywidgets 7.x
##@register("jupyter-exa.TestDOMWidget")    # ipywidgets 6.x
##class TestDOMWidget(DOMWidget):
##    """
##    A test widget that displays text and tests bidirectional communication
##    between Python and JavaScript.
##    """
##    _view_name = Unicode("TestDOMWidgetView").tag(sync=True)
##    _model_name = Unicode("TestDOMWidgetModel").tag(sync=True)
##    frontend_text = Unicode("Hello World!").tag(sync=True)
##    #backend_counter = Int(0).tag(sync=True)
##
##    def handle_msg(self, *args, **kwargs):
##        self.received = True
##
##    def __init__(self, *args, **kwargs):
##        super(TestDOMWidget, self).__init__(*args, **kwargs)
##        self.received = False
##
##
###@register                          # ipywidgets 7.x
##@register("jupyter-exa.TestKontainer")    # ipywidgets 6.x
##class TestKontainer(Container, TestDOMWidget):
##    """Widget container."""
##    _view_name = Unicode("TestKontainerView").tag(sync=True)
##    _model_name = Unicode("TestKontainerModel").tag(sync=True)
#
#
##class TestWidgets(TestCase):
##    """
##    Since command line unittests don't check for widget visibility, this test
##    checks for roundtrip messages going from Python to JavaScript and back.
##    """
##    def setUp(self):
##        """Execute the notebook."""
##        try:
##            check_call(["jupyter", "nbconvert", "--exec",
##                        "--ExecutePreprocessor.kernel_name=python", nbpath], cwd=cwd, **prckws)
##        except AssertionError:
##            try:
##                check_call(["jupyter", "nbconvert", "--exec",
##                            "--ExecutePreprocessor.kernel_name=python2", nbpath], cwd=cwd, **prckws)
##            except AssertionError:
##                try:
##                    check_call(["jupyter", "nbconvert", "--exec",
##                                "--ExecutePreprocessor.kernel_name=python3", nbpath], cwd=cwd, **prckws)
##                except Exception as e:
##                    self.fail(msg=str(e))
##
##    def test_value_check(self):
##        """Check bidirectional communication."""
##        try:
##            with open(tmppath) as f:
##                result = [line.strip() for line in f.readlines()]
##            #self.assertListEqual(result, expected)
##        except Exception as e:
##            self.fail(msg=str(e))
##
##    def tearDown(self):
##        """Cleanup the generated file."""
##        try:
##            os.remove(tmppath)
##            os.remove(htmlpath)
##        except Exception as e:
##            self.fail(msg=str(e))
