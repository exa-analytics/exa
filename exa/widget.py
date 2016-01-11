# -*- coding: utf-8 -*-
'''
Widget
=======================
The workspace is a way to track and interact with different sets of
:class:`~exa.relational.Session` objects, which themselves that keep track of
user work. This includes :class:`~exa.relational.Program`s,
:class:`~exa.relational.Project`s, :class:`~exa.relational.Job`s,
:class:`~exa.relational.File`s, and :class:`~exa.relational.Container`s.
'''
from ipywidgets import DOMWidget
from traitlets import Unicode


class Widget(DOMWidget):
    '''
    '''
    _view_module = Unicode('nbextensions/exa/static/js/exa.dashboard.widget', sync=True)
    _view_name = Unicode('DashboardView', sync=True)

    def __init__(self):
        super().__init__()
