#    -*- coding: utf-8 -*-
'''
Jupter Notebook Widget
=================================================
Entry point for communication between Python and the `Jupyter`_ notebook
`widgets`_ (JS).

See Also:
    :class:`~exa.dashboard.Dashboard`

.. _Jupyter: http://jupyter.org
.. widgets: https://ipywidgets.readthedocs.org/en/latest
'''
from ipywidgets import DOMWidget
from traitlets import Unicode


class DashboardWidget(DOMWidget):
    '''
    Generic Javascript widget.

    Attributes
        frame (int): This keeps track of the time index (if available)
        width (int): Widget width (in pixels)
        height (int): Widget height (in pixels)
        fps (int): Widget frames per second (for animation)
    '''
    _view_module = Unicode('nbextensions/exa/exa.dashboard.widget', sync=True)
    _view_name = Unicode('DashboardView', sync=True)

    def __init__(self):
        super().__init__()
