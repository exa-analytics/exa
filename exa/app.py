# -*- coding: utf-8 -*-
'''
Web Application
==================================
Entry point for communication between Python and the standalone exa web
application (HTML/CSS/JS).
'''
import os
from tornado.web import Application, RequestHandler
from tornado.template import Loader
from tornado.ioloop import IOLoop
from jinja2 import Environment, FileSystemLoader
from exa import Config
from exa.utils import mkpath


class HelloWorldHandler(RequestHandler):
    '''
    '''
    def get(self):
        self.write('Hello World')


class DashboardHandler(RequestHandler):
    '''
    '''
    def get(self):
        self.write(jinja2_loader.get_template('dashboard.html').render(**kwargs))


def serve(host='localhost', port=8080):
    '''
    '''
    exa_web_app.listen(port)
    IOLoop.instance().start()


def build_static_path_kwargs():
    '''
    '''
    kwargs = {}
    for root, subdirs, files in os.walk(Config.static):
        splitdir = root.split(Config.static)[1]
        directory = 'static'
        if splitdir:
            directory = directory + splitdir
        for name in files:
            n = name.replace('.', '_')
            n = n.replace('-', '_')
            kwargs[n] = '\'' + mkpath(directory, name) + '\''
    return kwargs


templates_path = Config.templates
static_path = Config.static
kwargs = build_static_path_kwargs()
print(kwargs)


tornado_settings = {
    'static_path': 'static'
}

tornado_handlers = [
    (r'/', DashboardHandler),
    (r'/hi', HelloWorldHandler)
]

jinja2_loader = Environment(loader=FileSystemLoader(searchpath=templates_path))

exa_web_app = Application(tornado_handlers, **tornado_settings)
