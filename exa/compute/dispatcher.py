# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Dispatch
########################
`Multiple dispatching`_ is a programming paradigm that delegates function calls
based on argument types. This is primarily a convenience for situations where
the behavior of a function or method may differ depending on argument types but
there is a desire to maintain a specific API. This is accomplished using the
:class:`~exa.compute.dispatcher.Dispatcher` which acts as a storage class for
dispatched functions with a given function name. Dispatched functions may be
designated using the convience decorator, :func:`~exa.compute.dispatcher.dispatch`,
as follows.

.. code-block:: python

    @dispatch(str)
    def f(x):
        return x.zfill(2)        # string operation

    @dispatch(int)
    def f(x):
        return x.bit_length()    # int operation

The implementation provided by this module allows for multiple function arguments,
each with multiple types.

.. code-block:: python

    @dispatch(str, (int, float))
    def f(x, y):
        return x.zfill(2), y.real

    @dispatch(int, str)
    def f(x, y):
        return x.bit_length(), y.zfill(3)

TODO additional features of dispatcher

Warning:
    Most syntax checkers, linters, or other code analyses methods will raise
    style or syntax errors on the code examples above. As always, use unit tests
    to ensure that code is behaving as expected.

.. _Multiple dispatching: https://en.wikipedia.org/wiki/Multiple_dispatch
"""
import numpy as np
from itertools import product
try:
    from inspect import signature
except ImportError:
    from inspect import getargspec as signature


_dispatched = {}    # Keeps track of all dispatched functions and methods
_ints = (int, np.int, np.int8, np.int16, np.int32, np.int64)
_floats = (float, np.float, np.float16, np.float32, np.float64)


class Dispatcher(object):
    """
    A class that represents a function with a given name and calls the correct
    method based on the signature of a given function call.
    """
    def register(self, func, *itypes, **flags):
        """Register a new function with a given signature."""
        nargs = get_nargs(func)
        ntyps = len(itypes)
        if nargs != ntyps:
            raise ValueError("Function has {} args but signature has {} entries!".format(nargs, ntyps))
        elif any(isinstance(typ, (tuple, list)) for typ in itypes):
            prod = []
            for typ in itypes:
                if isinstance(typ, (tuple, list)):
                    prod.append(typ)
                else:
                    prod.append(tuple([typ, ]))
            for typs in product(*prod):    # Recursive call to self.register
                self.register(func, *typs, **flags)
            return                         # Make sure to exit recursive calls
        # Begin registration process here, checking expanded arguments
        for typ in itypes:
            if not isinstance(typ, type):
                raise TypeError("Not a type: {}".format(typ))

    def __call__(self, *args, **kwargs):
        itypes = tuple([type(arg) for arg in args])
        sig = ("cpu", "ram", "serial", ) + itypes
        try:
            func = self.functions[sig]
        except KeyError as e:
            raise e
        return func(*args, **kwargs)

    def __init__(self, name):
        self.name = name
        self.__name__ = name
        self.functions = dict()
        if name not in _dispatched:
            _dispatched[name] = self

    def __repr__(self):
        return self.functions.__repr__()

    def __str__(self):
        return self.__repr__()

    def _html_repr_(self):
        pass


def dispatch(*itypes, **flags):
    """
    A high level decorator that creates a :class:`~exa.compute.dispatch.Dispatcher`
    callable (which behaves just like a function).

    This decorator wraps a number of other decorators into one simple API. For
    details see :func:`~exa.compute.compilers.wrapper.returns`,
    :func:`~exa.compute.compilers.wrapper.compile_function`, and
    :func:`~exa.compute.resources.autoparallel`.

    .. code-block:: Python

        @dispatch(int, float)
        def f(x, y):
            return x + y

        @dispatch(int, str)
        def f(x, y):
            return str(x) + y + "!"

    Args:
        itypes (tuple): Tuple of argument types
        compiler (str): See :func:`~exa.compute.compilers.wrapper.available_compilers`
        processing (str): One, or combination of "cpu", "gpu"
        memory (str): One, or combination of "ram", "disk"
        parallelism (str): One, or combination of "serial", "gilfree", "resources"
        otypes (tuple): Tuple of output type(s) or None
    """
    def dispatched_func(func):
        name = func.__name__                 # Checks to see if we have made
        if name in _dispatched:              # an entry for a function with the
            dispatcher = _dispatched[name]   # same name, creates one if not,
        else:                                # and registers the current function
            dispatcher = Dispatcher(name)    # definition to the provided types.
        dispatcher.register(func, *itypes, **flags)
        return dispatcher
    return dispatched_func


def get_nargs(func):
    """Get the count of function args."""
    spec = signature(func)
    if hasattr(spec, "parameters"):
        return len(spec.parameters.keys())
    return len(spec.args)
