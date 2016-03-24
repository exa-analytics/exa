# -*- coding: utf-8 -*-
'''
Container (Widget)
=======================
Functionality for using Jupyter notebook extensions to visualize data containers.
'''
import numpy as np
import pandas as pd
from ipywidgets import DOMWidget
from traitlets import Instance, Type, Any, Float, Int
from traitlets import Unicode, List, Integer, Bytes, CUnicode, Set, Tuple, Dict


class Widget(DOMWidget):
    '''
    Provides a custom Jupyter notebook widget class.
    '''
    _view_module = Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = Unicode('ContainerView').tag(sync=True)
    width = Integer(850).tag(sync=True)
    height = Integer(500).tag(sync=True)
    fps = Integer(24).tag(sync=True)
    test_3D = Unicode(pd.DataFrame(np.random.randint(-5, 5, size=(10, 3)),
                                   columns=('x', 'y', 'z')).to_json(orient='values')).tag(sync=True)
    #test_2D = Unicode(pd.DataFrame(np.random.randint(-20, 20, size=(20, 2)),
    #                               columns=('x', 'y')).to_json(orient='values')).tag(sync=True)
    #test_diameter = Float(4.2).tag(sync=True)

    def _handle_custom_msg(self, *args, **kwargs):
        '''
        Recieve and dispatch messages from the JavaScript frontend to the
        Python backend.
        '''
        print(args)
        print(kwargs)

    def _repr_html_(self):
        return self._ipython_display_()


class ContainerWidget(Widget):
    '''
    Specific implementation used by :class:`~exa.container.BaseContainer` and
    :class:`~exa.relational.container.Container`.

    Attributes:
        _names (list): List of all traits associated with the :class:`~exa.widget.ContainerWidget`
    '''
    gui_width = Integer(250).tag(sync=True)

    def __init__(self, container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container
