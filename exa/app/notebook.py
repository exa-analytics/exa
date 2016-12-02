# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Notebook Application Wrapper
#############################
"""
from notebook.notebookapp import NotebookApp
from exa._config import config


class ExaNotebook(NotebookApp):
    @classmethod
    def launch_instance(self, **kwargs):
        argv = [config['paths']['notebooks']]
        super(ExaNotebook, self).launch_instance(argv, **kwargs)
