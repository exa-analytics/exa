#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Application
##############
"""
from traitlets import Unicode
from notebook.notebookapp import NotebookApp


class Application(NotebookApp):
    description = """
    Docstring
    """

    default_url = Unicode("/app", config=True, help="")


main = launch_new_instance = Application.launch_instance
