# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa Notebook App
#############################
This module provides a wrapper around the `Jupyter notebook`_ that creates an
indexed and searchable set of notebook files based on :mod:`~exa.cms.__init__`.
"""
from notebook.notebookapp import NotebookApp
from exa._config import config


class ExaNotebook(NotebookApp):
    @classmethod
    def launch_instance(self, **kwargs):
        argv = [config['paths']['notebooks']]
        super(ExaNotebook, self).launch_instance(argv, **kwargs)
