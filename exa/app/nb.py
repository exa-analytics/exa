# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Notebook
#############################
Exa launches a `Jupyter notebook` in its root directory where all data and other
notebooks are stored.

.. _Jupyter notebook: http://jupyter.org/
"""
from notebook.notebookapp import NotebookApp
from exa._config import config


# TODO: Add custom styling to this notebook
# TODO: Add custom indexing of notebooks related to projects/
class Notebook(NotebookApp):
    """Launch the notebook app in the exa directory."""
    @classmethod
    def launch_instance(self, **kwargs):
        argv = [config['paths']['notebooks']]
        super(Notebook, self).launch_instance(argv, **kwargs)
