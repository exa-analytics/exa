# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Dispatched Functions
########################
This module provides the :class:`~exa.compute.dispatch.Dispatcher` object
and the :func:`~exa.compute.dispatch.dispatch` decorator. The primary purpose of
the dispatcher is to allow for the `multiply dispatched`_ programming paradigm.
Because "dispatching" requires information about argument types, it is
convenient to also perform dynamic compilation upon dispatch. Compilation can
allow for GIL free execution enabling parallelization. Of course, it also
usually makes the function faster. See :mod:`~exa.compute.compilation` for
more information.

Warning:
    Most syntax checkers, linters, or other code analyses methods will raise
    style or syntax errors on the code examples above. As always, use unit tests
    to ensure that code is behaving as expected.

.. _numba: http://numba.pydata.org/
.. _multiply dispatched: https://en.wikipedia.org/wiki/Multiple_dispatch
"""
import numpy as np
from itertools import product
try:
    from inspect import signature
except ImportError:
    from inspect import getargspec as signature
#from exa.compute.compiler import compile_function


_dispatched = dict()    # Global to keep track of all dispatched functions
ints = (int, np.int8, np.int16, np.int32, np.int64)
floats = (float, np.float16, np.float32, np.float64)


class Dispatcher(object):
    """
    A class for storing type dispatched functions.

    .. code-block:: Python

        @dispatch(str)
        def fn(arg):
            return arg + "!"

        @dispatch(int)
        def fn(arg):
            return str(2*arg) + "!"

        @dispatch(float)
        def fn(arg):
            return str(20*arg) + "!"

    This example generates a function dispatcher that makes a call to the appropriate
    function signature depending on the type of the argument given. For cases where
    the same signature supports multiple argument types the following syntax is
    acceptable.

    .. code-block:: Python

        @dispatch((str, int))
        def fn(arg):
            return str(arg) + "!"

        @dispatch((bool, float))
        def fn(arg):
            return str(float(arg)*42) + "!"

    In these examples, signature references will be created for both types of
    arguments passed to the dispatch decorator.
    """
    def register(self, func, *itypes, **flags):
        """
        Register a new function signature.
        """
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
        #sig, func = compile_function(func, *itypes, **flags)
        #self.functions[sig] = func

    @property
    def signatures(self):
        """
        Check avaiable function signatures.

        Returns:
            df (:class:`~pandas.DataFrame`): Data table of available signatures
        """
        return False

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

    def _repr_html_(self):
        return self.to_frame()._repr_html_()


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
