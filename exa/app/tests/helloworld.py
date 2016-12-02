# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Hello World
#################
"""
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler


class Handler(RequestHandler):
    """
    """
    def get(self):
        self.write("Hello world!")


webapp = Application([(r"/", Handler)])
