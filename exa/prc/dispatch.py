# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Dispatched Functions
########################
This module provides the :class:`~exa.workflow.dispatcher.Dispatcher` object
and the :func:`~exa.workflow.dispatcher.dispatch` decorator. The purpose of the
dispatcher is not only to enable a `multiply dispatched`_ paradigm but also to
compile functions compatible with :class:`~exa.prc.workflow.Workflow` class.
Compilation is performed by `numba`_ if available.

.. _numba: http://numba.pydata.org/
.. _multiply dispatched: https://en.wikipedia.org/wiki/Multiple_dispatch
"""
import numpy as np
import pandas as pd
from sys import getsizeof
from itertools import product
from exa._config import config
try:
    import numba as nb    # Don't make numba a hard dependency
except ImportError:
    nb = None
try:
    from inspect import signature
except ImportError:
    from inspect import getargspec as signature


_dispatched = dict()    # Global to keep track of all dispatched functions


class Dispatcher:
    """
    Class that wraps functions with specific argument types into a single,
    multiply dispatched interface.
    """
    @property
    def avail(self):
        """Check avaiable function signatures."""
        proc = []
        mem = []
        parallel = []
        types = []
        exists = []
        for sig in self.functions.keys():
            p, m, l = sig[:3]
            typ = tuple(sig[3:])
            proc.append(p)
            mem.append(m)
            parallel.append(l)
            types.append("(" + ", ".join([t.__name__ for t in typ]) + ")")
            exists.append(True)
        df = pd.DataFrame.from_dict({'types': types, 'proc': proc, 'mem': mem,
                                     'parallel': parallel, 'exists': exists})
        df = df.pivot_table(values='exists', index=['proc', 'mem', 'parallel'],
                            columns='types')
        df.fillna(False, inplace=True)
        return df

    def register(self, types, func, layout=None, jit=False, vectorize=False,
                 nopython=False, nogil=False, cache=False, rtype=None,
                 target='cpu', outcore=False, distrib=False):
        """
        Register a new function signature.

        In addition to accepting the required types (function signature), this
        method can request the function be compiled according to option arguments
        specified.

        Args:
            types (tuple): Type(s) for each argument
            func (function): Function to be registered
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
        ntyps = len(types)
        if nargs != ntyps:
            raise ValueError("Function has {} args but signature has {} entries!".format(nargs, ntyps))
        elif any(isinstance(typ, (tuple, list)) for typ in types):
            prod = []
            for typ in types:
                if not isinstance(typ, (tuple, list)):
                    prod.append([typ])
                else:
                    prod.append(typ)
            for typs in product(*prod):
                self.register(typs, func, jit=jit, vectorize=vectorize,
                              nopython=nopython, nogil=nogil, cache=cache)
            return
        for typ in types:
            if not isinstance(typ, type):
                raise TypeError("Not a type: {}".format(typ))
        sig = [0, 0, 0]
        if outcore:
            sig[1] = 1
        if nogil or vectorize:
            sig[2] = 1
        if distrib:
            sig[2] = 2
        if target == 'cuda':
            sig[0] = 1
        sig = tuple(sig)
        sig += types
        if jit and nb is not None:
            self.functions[sig] = func
        elif vectorize and nb is not None:
            self.functions[sig] = func
        else:
            self.functions[sig] = func

    @property
    def __doc__(self):
        doc = "Dispatched method {}".format(self.name)
        for func in self.functions.values():
            doc += func.__doc__
            doc += "="*80 + r"\n\n"
        return doc

    def __call__(self, *args, **kwargs):
        sig = (0, 0, 0, )
        types = tuple([type(arg) for arg in args])
        memlim = kwargs.pop("_memlim", 2048)
        nodes = kwargs.pop("_nodes", list())
        proc = 1 if config['dynamic']['cuda'] == 'true' else 0
        size = sum(getsizeof(arg) for arg in args)
        mem = 1 if size/1024**2 > memlim else 0
        pll = 0
        if len(nodes) > 0:
            pll = 2
        elif any(key[1] > 0 for key in self.functions.keys()):
            pll = 1
        sig = (proc, mem, pll, ) + types
        try:
            func = self.functions[sig]
        except KeyError:
            raise KeyError("Missing signature for {}".format(sig))
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


def dispatch(*types, **flags):
    """
    Decorator used to create/register a strongly typed and possibly parallelized
    and/or compiled function for standalone use or as part of a
    :class:`~exa.workflow.Workflow`. For a description of the arguments and
    usage examples see :class:`~exa.workflow.dispatch.Dispatcher`.
    """
    def dispatched_func(func):
        name = func.__name__
        if name in _dispatched:
            dispatcher = _dispatched[name]
        else:
            dispatcher = Dispatcher(name)
        dispatcher.register(types, func, **flags)
        return dispatcher
    return dispatched_func

def get_nargs(func):
    """
    Get the count of function args.
    """
    spec = signature(func)
    if hasattr(spec, "parameters"):
        return len(spec.parameters.keys())
    return len(spec.args)
