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
from exa import Config


class Widget(DOMWidget):
    '''
    '''
    _view_module = Unicode('nbextensions/exa/static/js/exa.dashboard.widget', sync=True)
    _view_name = Unicode('DashboardView', sync=True)
