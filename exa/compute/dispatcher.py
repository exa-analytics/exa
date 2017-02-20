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

    @dispatch
    def f(


TODO additional features of dispatcher

Warning:
    Most syntax checkers, linters, or other code analyses methods will raise
    style or syntax errors on the code examples above. As always, use unit tests
    to ensure that code is behaving as expected.

.. _Multiple dispatching: https://en.wikipedia.org/wiki/Multiple_dispatch
"""
from itertools import product
try:
    from inspect import signature
except ImportError:
    from inspect import getargspec as signature


_dispatched = {}    # Keeps track of all dispatched functions and methods


class Dispatcher(object):
    """
    A class that represents a function with a given name and calls the correct
    method based on the signature of a given function call.
    """
    def register(self, f, *args, **kwargs):
        """
        Register a new function signature.

        Args:
            f (callable): A callable function or method
        """
        print(args, kwargs)

#        nargs = get_nargs(func)
#        ntyps = len(itypes)
#        if nargs != ntyps:
#            raise ValueError("Function has {} args but signature has {} entries!".format(nargs, ntyps))
#        elif any(isinstance(typ, (tuple, list)) for typ in itypes):
#            prod = []
#            for typ in itypes:
#                if isinstance(typ, (tuple, list)):
#                    prod.append(typ)
#                else:
#                    prod.append(tuple([typ, ]))
#            for typs in product(*prod):    # Recursive call to self.register
#                self.register(func, *typs, **flags)
#            return                         # Make sure to exit recursive calls
#        # Begin registration process here, checking expanded arguments
#        for typ in itypes:
#            if not isinstance(typ, type):
#                raise TypeError("Not a type: {}".format(typ))

    def __call__(self, *args, **kwargs):
        """
        Compute the function signature based on argument types and call the
        correct function signature.
        """
        pass

    def __new__(cls, name):
        """
        Checks if to see if a dispatcher with the given name has been created,
        if it has return it, otherwise create a new dispatcher object.
        """
        return _dispatched.get(name, cls)

    def __init__(self, name):
        self.name = name
        self.__name__ = name
        self.functions = {}
        _dispatched[name] = self

    def __repr__(self):
        return self.functions.__repr__()

    def __str__(self):
        return self.__repr__()


def dispatch(*args, **kwargs):
    """
    A decorator for enabling the multiple dispatch paradigm.

    This function creates a :class:`~exa.compute.dispatch.Dispatcher` object.
    This object is a callable that delegates to the correct (registered)
    function based on the signature of the arguments passed.

    .. code-block:: python

        @dispatch          # No type arguments
        def f(a, b=None):
            return a, b

        @dispatch
    """
    #if len(args) == 1 and callable(args[0]):    # No types passed, assumed default arg


    def registered(f):
        dispatcher = _dispatched[f.__name__]        # Get or create dispatcher
        dispatcher.register(f, *itypes, **flags)    # Register signatures
        return dispatcher
    return registered


def arg_count(f):
    """Return argument count, len(args) + len(kwargs), to the function."""
    spec = signature(f)
    if hasattr(spec, "parameters"):
        return len(spec.parameters.keys())
    return len(spec.args)
