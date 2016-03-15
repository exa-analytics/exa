# -*- coding: utf-8 -*-
'''
Container (Widget)
=======================
Functionality for using Jupyter notebook extensions to visualize data containers.
'''
from ipywidgets import DOMWidget
from traitlets import Unicode, Integer


class Widget(DOMWidget):
    '''
    Provides a custom Jupyter notebook widget class.
    '''
    _view_module = Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = Unicode('ContainerView').tag(sync=True)
    _ipy_disp = DOMWidget._ipython_display_
    width = Integer(850).tag(sync=True)
    height = Integer(500).tag(sync=True)
    gui_width = Integer(250).tag(sync=True)
    fps = Integer(24).tag(sync=True)

    def __init__(self, container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container
