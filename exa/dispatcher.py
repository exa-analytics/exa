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
    def register(self, f, core=False, threaded=False, nogil=False, cuda=False, *args, **kwargs):
        """
        Register a new function signature.

        Args:
            f (callable): A callable function or method
            core (bool): Wrap as out of core function
            thread (bool): Compile multi-threaded function
            nogil (bool): Compile `GIL`_ free function
            cuda (bool): Compile function for GPU execution
            args: Function argument types
            kwargs: Function argument types and flags
        """
        print("register: ", f, args, kwargs)
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


def dispatch(core=False, thread=False, nogil=False, cuda=False, *args, **kwargs):
    """
    Dispatch a function or method.

    Basic usage is as follows.

    .. code-block:: python

        @dispatch
        def f(a):
            pass

        @dispatch
        def f(a: type) -> type:    # Python 3 only
            pass

        @dispatch(type)
        def f(a):
            pass

    Args:
        core (bool): Wrap as out of core function
        thread (bool): Compile multi-threaded function
        nogil (bool): Compile `GIL`_ free function
        cuda (bool): Compile function for GPU execution

    Note:
        Compiling a threaded function automatically releases the `GIL`_.

    .. _GIL: https://en.wikipedia.org/wiki/Global_interpreter_lock
    """
    def create(fn, core, nogil, threaded, cuda, *args, **kwargs):
        """
        Generate (or get) the :class:`~exa.compute.dispatcher.Dispatcher`
        object and register the new signature.
        """
        dsptchr = Dispatcher(fn.__name__)
        dsptchr.register(fn, core=core, threaded=threaded, nogil=nogil, cuda=cuda, *args, **kwargs)
        return dsptchr

    def helper(fn):
        """
        Helper function that wraps :func:`~exa.compute.dispatcher.dispatch` and
        calls the ``create`` function correctly.
        """
        return processor(fn, core, nogil, threaded, cuda, *args, **kwargs)

    # Extract the correct arugments and process the function
    # If no explicit type hints given
    if (len(args) == 1 and len(kwargs) == 0 and callable(args[0])
        and not isinstance(args[0], type)):
        f = args[0]
        return processor(f, core, nogil, threaded, cuda, **kwargs)
    else:
        return helper    # Explicit/implicit type hints given


def arg_count(f):
    """Return argument count, len(args) + len(kwargs), to the function."""
    spec = signature(f)
    if hasattr(spec, "parameters"):
        return len(spec.parameters.keys())
    return len(spec.args)
