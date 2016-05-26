# -*- coding: utf-8 -*-
'''
Main
==================================
'''
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop


class MainEntryHandler(RequestHandler):
    def get(self):
        self.write('Hello world!')


def serve(port):
    '''
    Serve the web application
    '''
    app.listen(port)
    IOLoop.instance().start()
    

app = Application([(r'/', MainEntryHandler), ])
