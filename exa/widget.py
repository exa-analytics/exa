# -*- coding: utf-8 -*-
'''
Container (Widget)
=======================
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
    Base class for creating data specific container widgets within a Jupyter
    notebook. The class provides some suitable defaults and custom methods for
    bidirectional communication (Python-Javascript), logging, and
    representation.
    '''
    width = Integer(850).tag(sync=True)
    height = Integer(500).tag(sync=True)
    fps = Integer(24).tag(sync=True)

    def _handle_custom_msg(self, *args, **kwargs):
        '''
        Recieve and dispatch messages from the JavaScript frontend to the
        Python backend.
        '''
        content = args[0]
        print(content, args, kwargs)

    def _repr_html_(self):
        return self._ipython_display_()


class ContainerWidget(Widget):
    '''
    Jupyter notebook widget representation of a
    :class:`~exa.container.BaseContainer` object.
    '''
    _view_module = Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = Unicode('ContainerView').tag(sync=True)
    gui_width = Integer(250).tag(sync=True)

    def __init__(self, container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container
