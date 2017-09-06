# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Singletons
#######################################
The `singleton`_ design pattern can be useful when only one instance of a class
is ever required.

.. _singleton: https://en.wikipedia.org/wiki/Singleton_pattern
"""
class Singleton(object):
    __classes = {}

    def __new__(cls, *args, **kwargs):
        clsid = hash(cls)
        if clsid not in cls.__classes:
            cls.__classes[clsid] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__classes[clsid]
