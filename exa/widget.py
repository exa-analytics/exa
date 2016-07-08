# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Widget
##################
Functionality for using Jupyter notebook extensions to visualize data speficic
containers.
'''
import os
import atexit
import shutil
import numpy as np
import pandas as pd
from ipywidgets import DOMWidget
from notebook import install_nbextension
from notebook.nbextensions import jupyter_data_dir
from traitlets import Unicode, Integer
from exa._config import config
from exa.utility import mkp


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


def install_notebook_widgets(pkg_nbext, sys_nbext, verbose=False):
    '''
    Convenience wrapper around :py:func:`~notebook.install_nbextension` that
    organizes notebook extensions for exa and related packages in a systematic
    fashion.

    Args:
        pkg_nbext (str): Path to the "_nbextension" directory in the source
        sys_nbext (str): Path to the system "nbextensions" directory
        verbose (bool): Verbose installation
    '''
    try:
        shutil.rmtree(sys_nbext)
    except FileNotFoundError:
        pass
    for root, subdirs, files in os.walk(pkg_nbext):
        for filename in files:
            subdir = root.split('_nbextension')[-1]
            orig = mkp(root, filename)
            dest = mkp(sys_nbext, subdir, mk=True)
            install_nbextension(orig, verbose=verbose, overwrite=True, nbextensions_dir=dest)


if config['js']['update'] == '1':
    verbose = True if config['log']['level'] != '0' else False
    pkg_nbext = mkp(config['dynamic']['pkgdir'], '_nbextension')
    sys_nbext = mkp(jupyter_data_dir(), 'nbextensions', 'exa')
    install_notebook_widgets(pkg_nbext, sys_nbext, verbose)
