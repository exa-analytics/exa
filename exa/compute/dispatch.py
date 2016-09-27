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
import pandas as pd
from itertools import product
try:
    from inspect import signature
except ImportError:
    from inspect import getargspec as signature
from exa.compute.compilation import compile_function


_dispatched = dict()    # Global to keep track of all dispatched functions


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

        In addition to accepting the required types (function signature), this
        method can request the function be compiled according to option arguments
        specified.

        Args:
            func (function): Function to be registered
            itypes (tuple): Type(s) for each argument
            otypes (tuple): Output type(s)
            layout (str): Dimensionality reduction/expansion layout
            jit (bool): Just-in-time function compilation
            vectorize (bool): Just-in-time function vectorization and compilation
            nopython (bool): Compile with native types (true) or Python types (false)
            nogil (bool): Release the GIL when compiling with native types
            cache (bool): Compile to disk based cache
            rtype (type): Vectorized return type
            target (str): Vectorized compile architecture target
            outcore (bool): If the function designed for out-of-core execution
            distrib (bool): True if function desiged for distributed execution
        """
        nargs = get_nargs(func)
        ntyps = len(itypes)
        if nargs != ntyps:
            raise ValueError("Function has {} args but signature has {} entries!".format(nargs, ntyps))
        elif any(isinstance(typ, (tuple, list)) for typ in itypes):
            prod = []
            for typ in itypes:
                if not isinstance(typ, (tuple, list)):
                    prod.append([typ])
                else:
                    prod.append(typ)
            for typs in product(*prod):
                self.register(func, *typs, **flags)
            return
        for typ in itypes:
            if not isinstance(typ, type):
                raise TypeError("Not a type: {}".format(typ))
        reg = (0, 0, 0, ) + itypes
        jit = flags.pop('jit', False)
        vectorize = flags.pop('vectorize', False)
        guvectorize = flags.pop('guvectorize', False)
        if jit or vectorize or guvectorize:
            reg, func = compile
        #if jit or vectorize or guvectorize:
        #    reg, func = compile_func(func)
        self.functions[reg] = func

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
        sig = (0, 0, 0, ) + itypes
        try:
            func = self.functions[sig]
        except KeyError:
            raise TypeError("No type signature for type(s) {}".format(sig))
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
    Decorator to transform a set of functions into a
    :class:`~exa.compute.dispatch.Dispatcher` callable (behaves just like a
    function).

    .. code-block:: Python

        @dispatch(int, float)
        def f(x, y):
            return x + y

        @dispatch(int, str)
        def f(x, y):
            return str(x) + y + "!"

    See Also:
        More examples can be found in the tests: :class:`~exa.compute.tests.test_dispatch`.
    """
    def dispatched_func(func):
        name = func.__name__                 # It checks to see if we have made
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
