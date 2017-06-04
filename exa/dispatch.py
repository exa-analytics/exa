# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Multiple Dispatch
#########################################
`Multiple dispatch`_ is a programming paradigm that delegates function calls
based on the (input) argument types; although the function has a single name,
the operational algorithm differs depending on the arguments types. Reasons
for maintaining a single name vary, but a common one is a desire to keep a
simple 'API'.

The dispatcher is a singleton factory that creates an instance of the
:class:`~exa.dispatch.Dispatcher` for every named function.
"""
from .single import Singleton


#class Dispatched(object):


class Dispatcher(Singleton):
    """
    Related to workflows?
    """
    pass
    #def __new__(mcs, *args, **kwargs):
    #    return super(Dispatcher, mcs).__new__(mcs, *args, **kwargs)

#    def __call__(self):
#        return self.fn()
#
#    def __init__(self, fn, *args, **kwargs):
#        self.fn = fn
