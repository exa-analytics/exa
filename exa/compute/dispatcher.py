# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Dispatch
########################
`Multiple dispatching`_ is a programming paradigm that delegates function calls
based on input argument types. This is primarily a convenience for situations
where the behavior of a function or method may differ depending on argument
types but there is a design goal to maintain a single API (i.e. function name).
In Python 2 or 3 the following syntax can be used.

.. code-block:: python

    @dispatch(str)        # If 'a' is a string
    def f(a):
        return a.zfill(2)

    @dispatch(int)        # If 'a' is an int
    def f(a):
        return a.bit_length()

    @dispatch             # No types - default function signature
    def f(a):
        return f(str(a))

Native `type hints`_ may be used instead, if working exclusively in Python 3.
Function signatures are extracted automatically from Python 3's type hinting
system.

.. code-block:: python

    import typing

    @dispatch
    def f(a: str) -> str:
        return a.zfill(2)

    MyType = typing.NewType('MyType', int0
    @dispatch
    def f(a: MyType) -> MyType:
        return a.bit_length()

    @dispatch
    def f(a: typing.Any) -> typing.Any:
        return f(str(a))

Warning:
    Type hinting is only available in Python 3. For backwards compatibility
    used the former syntax for declaring function signatures.

Dispatching is accomplished via the :class:`~exa.compute.dispatcher.Dispatcher`
which acts as a dictionary of function signature keys and callable values. The
:func:`~exa.compute.dispatcher.dispatch` decorator is provided for most use
cases but 'by hand' creation of dispatched functions is also possible (see the
tests, :mod:`~exa.compute.tests.test_dispatcher` for an example).

Finally, both the decorator and dispatcher class accept additional keyword
arguments that can be used to improve function performance.
TODO additional features of dispatcher
- out of core (dask)
- gil free (numba)
- threaded (numba)
- gpu (numba/accelerate?)

.. _Multiple dispatching: https://en.wikipedia.org/wiki/Multiple_dispatch
.. _type hints: https://docs.python.org/3/library/typing.html
"""
from functools import wraps
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
    i = 0
    def register(self, f, *args, **kwargs):
        """
        Register a new function signature.

        Args:
            f (callable): A callable function or method
            args: Function argument types
            kwargs: Function argument types and flags
        """
        print("reg: ", f, args, kwargs)
        self.functions[self.i] = f
        self.i += 1

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
        return _dispatched.get(name, super(Dispatcher, cls).__new__(cls))

    def __init__(self, name):
        self.name = name
        self.__name__ = name
        self.functions = {}
        _dispatched[name] = self


def dispatch(*args, **kwargs):
    """A decorator for dispatching functions."""
    print("1: ", args, kwargs)
    def wrapper(f, *args, **kwargs):
        print("2: ", f, args, kwargs)
        return f

    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        print(args[0])
        return args[0]
    else:
        print(wrapper)
        return wrapper

#    def wrapper(*args, **kwargs):
#        """
#        A helper decorator to manage additional flags that may be passed along
#        with the function to modify dispatching.
#        """
#        ooc = kwargs.pop('ooc', False)
#        nogil = kwargs.pop('nogil', False)
#        threaded = kwargs.pop('threaded', False)
#        cuda = kwargs.pop('cuda', False)
#        # Now get the correct arguments for registration
#        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
#            print("2: ", args, kwargs)
#            args = list(args)
#            f = args.pop(0)
#        else:
#            f = wrapper
#        print(f.__name__, f, args, kwargs, ooc, nogil, threaded, cuda)
#        dspchr = Dispatcher(f.__name__)
#        print("dispatcher: ", dspchr)
#        dspchr.register(f, ooc=ooc, nogil=nogil, threaded=threaded, cuda=cuda, **kwargs)
#        return dspchr
#    return wrapper


def arg_count(f):
    """Return argument count, len(args) + len(kwargs), to the function."""
    spec = signature(f)
    if hasattr(spec, "parameters"):
        return len(spec.parameters.keys())
    return len(spec.args)
