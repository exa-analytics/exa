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
    def register(self, f, *args, **kwargs):
        """
        Register a new function signature.

        Args:
            f (callable): A callable function or method
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
        print("newing: ", name)
        return _dispatched.get(name, super(Dispatcher, cls).__new__(cls))

    def __init__(self, name):
        print("initing: ", name)
        self.name = name
        self.__name__ = name
        self.functions = {}
        _dispatched[name] = self


#def dispatch(core=False, thread=False, nogil=False, cuda=False,
#             *args, **kwargs):
#    """
#    Dispatch a function or method.
#
#    Basic usage is as follows.
#
#    .. code-block:: python
#
#        @dispatch
#        def f(a):
#            pass
#
#        @dispatch
#        def f(a: type) -> type:    # Python 3 only
#            pass
#
#        @dispatch(type)
#        def f(a):
#            pass
#
#    Args:
#        core (bool): Wrap as out of core function
#        thread (bool): Compile multi-threaded function
#        nogil (bool): Compile `GIL`_ free function
#        cuda (bool): Compile function for GPU execution
#
#    Note:
#        Compiling a threaded function automatically releases the `GIL`_.
#
#    .. _GIL: https://en.wikipedia.org/wiki/Global_interpreter_lock
#    """
#
#
#def processor(fn, core, nogil, threaded, cuda, *args, **kwargs):
#print("5: Processor", fn, args, kwargs)
#return fn
#def helper(fn):
#print("helping? ", fn, fn.__name__)
#if hasattr(fn, "__annotations__"):
#kwargs.update(fn.__annotations__)
#return processor(fn, core, nogil, threaded, cuda, *args, **kwargs)
## Extract the correct arugments
## Remove flags
#core = kwargs.pop('ooc', False)
#nogil = kwargs.pop('nogil', False)
#threaded = kwargs.pop('threaded', False)
#cuda = kwargs.pop('cuda', False)
## args and kwargs only have types and a function arguments now
## If no type hints passed
#print("1: ", args, kwargs, core, nogil, threaded, cuda)
#if (len(args) == 1 and len(kwargs) == 0 and callable(args[0])
#and not isinstance(args[0], type)):
#f = args[0]
#if not hasattr(f, "__annotations__") or len(f.__annotations__) == 0:
#print("2: No type hints")
#return processor(f, core, nogil, threaded, cuda)
#else:
#print("3: __annotations__ type hints")
#kwargs = {name: typ for name, typ in f.__annotations__.items() if name != "return"}
#return processor(f, core, nogil, threaded, cuda, **kwargs)
#else:
#print("4: args/kwargs type hints (and annotations?)")
#return helper
#
#
#
#def dispatch(*args, **kwargs):
#    """Dispatch a function or method."""
#    print("1: ", args, kwargs)
#    def processor(fn, *types, **flags):
#
#    def decorator(fn):
#        print("2: ", fn)
#        dspchr = Dispatcher(fn.__name__)    # Get or create Dispatcher
#        dspchr.register(fn)
#        return dspchr
#
#    if (len(args) == 1 and len(kwargs) == 0 and callable(args[0])
#        and not isinstance(args[0], type)):
#        print("3: No args")
#        return decorator(args[0])
#    else:
#        print("4: args")
#        return decorator
#
##    def wrapper(*args, **kwargs):
##        """
##        A helper decorator to manage additional flags that may be passed along
##        with the function to modify dispatching.
##        """
##        ooc = kwargs.pop('ooc', False)
##        nogil = kwargs.pop('nogil', False)
##        threaded = kwargs.pop('threaded', False)
##        cuda = kwargs.pop('cuda', False)
##        # Now get the correct arguments for registration
##        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
##            print("2: ", args, kwargs)
##            args = list(args)
##            f = args.pop(0)
##        else:
##            f = wrapper
##        print(f.__name__, f, args, kwargs, ooc, nogil, threaded, cuda)
##        dspchr = Dispatcher(f.__name__)
##        print("dispatcher: ", dspchr)
##        dspchr.register(f, ooc=ooc, nogil=nogil, threaded=threaded, cuda=cuda, **kwargs)
##        return dspchr
##    return wrapper


def arg_count(f):
    """Return argument count, len(args) + len(kwargs), to the function."""
    spec = signature(f)
    if hasattr(spec, "parameters"):
        return len(spec.parameters.keys())
    return len(spec.args)
