#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Web Application
##################
"""
from jinja2 import FileSystemLoader
from notebook.base.handlers import IPythonHandler


cwd = os.path.dirname(__file__)
file_loader = FileSystemLoader(cwd)


class MainHandler(IPythonHandler):
    """
    """
    @authenticated
    def get(self):
        self.write(self.render_template("templates/main.html"))

    def get_template(self, name):
        return file_loader.load(self.settings['jinja2_env'], name)

default_handlers = [
    (PREFIX + r'/?', MainHandler),
]
