# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Special Functions
#########################################
This module provides the :class:`~exa.functions.LazyFunction` class. This class
behaves like a function but accepts arguments for future evaluation (i.e. lazy
evaluation).

See Also:
    The :class:`~exa.dispatch.Dispatcher` takes advantage of lazy evaluation.
"""


class LazyFunction(object):
    """
    A class that behaves like a function and supports lazy evaluation.

    .. code-block:: python

        # Processing code ...
        # ... build our functions now because we
        # know the value of n currently ...
        fs = []
        for i in range(n):
            fs.append(LazyFunction(lambda x: x**2 + x**3 + x**4, x=i))
        # ... continue processing ...
        # ... at some later time (when needed)
        # evalulate the functions.
        results = [f() for f in fs]
    """
    def __call__(self, **kwargs):
        """Evaluate the function and return the results."""
        kws = dict(self.kwargs)
        kws.update(kwargs)
        return self.fn(*self.args, **kws)

    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        fmt = "{}(fn={}, nargs={}, nkwargs={})".format
        return fmt(self.__class__.__name__, self.fn.__name__,
                   len(self.args), len(self.kwargs))
