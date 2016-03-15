# -*- coding: utf-8 -*-
'''
Container (Widget)
=======================
Functionality for using Jupyter notebook extensions to visualize data containers.
'''
from ipywidgets import DOMWidget
from traitlets import Unicode, Integer, MetaHasTraits
from exa.relational.base import BaseMeta


class Widget(DOMWidget):
    '''
    Data container widget subclass.

    This class is subclassed by :class:`~exa.container.WidgetContainer` in
    order to enable interactive data visualize within the Jupyter notebook
    environment.
    '''
    _view_module = Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = Unicode('ContainerView').tag(sync=True)
    _ipy_disp = DOMWidget._ipython_display_
    width = Integer(850).tag(sync=True)
    height = Integer(500).tag(sync=True)
    gui_width = Integer(250).tag(sync=True)
    fps = Integer(24).tag(sync=True)


class _Meta(MetaHasTraits, BaseMeta):
    '''
    A dummy metaclass to enable inheritence from both :class:`~ipywidget.DOMWidget`
    and :class:`~exa.relational.RelationalContainer`.
    '''
    pass
