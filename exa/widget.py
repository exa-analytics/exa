# -*- coding: utf-8 -*-
'''
Base Widget
##################
Functionality for using Jupyter notebook extensions to visualize data speficic
containers.
'''
import numpy as np
import pandas as pd
from ipywidgets import DOMWidget
from traitlets import Instance, Type, Any, Float, Int
from traitlets import Unicode, List, Integer, Bytes, CUnicode, Set, Tuple, Dict


class Widget(DOMWidget):
    '''
    Base widget class for Jupyter notebook widgets provided by exa. Standardizes
    bidirectional communication handling between notebook extensions' frontend
    JavaScript and backend Python.
    '''
    width = Integer(850).tag(sync=True)
    height = Integer(500).tag(sync=True)
    fps = Integer(24).tag(sync=True)

    def _handle_custom_msg(self, message, callback):
        '''
        Recieve and handle messages from notebook extensions ("frontend").
        '''
        raise NotImplementedError('Handling custom message from JS not ready')
        typ = data['type']
        content = data['content']
        # Logic to handle various types of messages...

    def _repr_html_(self):
        return self._ipython_display_()


class ContainerWidget(Widget):
    '''
    Jupyter notebook widget representation of an exa Container. The widget
    accepts a (reference to a) container and parameters and creates a suitable
    display. By default a container displays an interactive graphic containing
    information provided by :func:`~exa.container.BaseContainer.info` and
    :func:`~exa.contianer.BaseContainer.network`.

    See Also:
        :mod:`~exa.container`, :mod:`~exa.relational.container`
    '''
    _view_module = Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = Unicode('ContainerView').tag(sync=True)
    gui_width = Integer(250).tag(sync=True)

    def __init__(self, container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container
        self.params = {'save_dir': '', 'file_name': ''}
