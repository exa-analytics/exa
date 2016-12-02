# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Web Application
#################
This module defines a `traitlets`_ based application that supports
"""
import webbrowser
from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from tornado.httpserver import HTTPServer
from traitlets.config import Application
from exa._version import __version__
from exa.app.tests.helloworld import webapp as default_webapp


class ExaApp(Application):
    description = """Extensible GUI for exa applications
    """
    examples = """
    """
    name = "exa"
    version = __version__

    @coroutine
    def start(self):
        self.http_server = HTTPServer(self.webapp)
        self.http_server.listen(self.port)
        self.ioloop = IOLoop.current()
        self.ioloop.start()


    def __init__(self, *args, **kwargs):
        port = kwargs.pop("port", 8080)
        webapp = kwargs.pop("webapp", None)
        super(ExaApp, self).__init__(*args, **kwargs)
        self.webapp = default_webapp if webapp is None else webapp
        self.port = port
        webbrowser.open_new_tab("http://localhost:{}".format(self.port))


#class ExaHub(Application):
#    description = """Multiuser exa hub
#    """
