# -*- coding: utf-8 -*-
'''
Container (Widget)
=======================
Functionality for using Jupyter notebook extensions to visualize data containers.
'''
from ipywidgets import DOMWidget
from traitlets import Unicode


class Widget(DOMWidget):
    '''
    '''
    _ipy_disp = DOMWidget._ipython_display_
    _view_module = traitlets.Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = traitlets.Unicode('ContainerView').tag(sync=True)
    width = traitlets.Integer(850).tag(sync=True)
    height = traitlets.Integer(500).tag(sync=True)
    _gui_width = traitlets.Integer(250).tag(sync=True)
    _fps = traitlets.Integer(24).tag(sync=True)
