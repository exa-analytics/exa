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
    width = Integer(850).tag(sync=True)
    height = Integer(500).tag(sync=True)
    fps = Integer(24).tag(sync=True)

    def _handle_custom_msg(self, *args, **kwargs):
        '''
        Recieve and dispatch messages from the JavaScript frontend to the
        Python backend.
        '''
        print(args)
        print(kwargs)
        raise NotImplementedError()

    def _repr_html_(self):
        return self._ipython_display_()


class ContainerWidget(Widget):
    '''
    Specific implementation used by :class:`~exa.container.BaseContainer` and
    :class:`~exa.relational.container.Container`.
    '''
    gui_width = Integer(250).tag(sync=True)
    
    def __init__(self, container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container
