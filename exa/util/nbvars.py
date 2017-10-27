# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Numba Extensions
####################
The `numba`_ package provides a mechanism for compiling Python code. With
appropriate options, compilation can provide massive speedups to standard
Python code. This module provides reasonable compilation options as well as
a utility for compiling symbolic (or string) functions to 'numbafied' functions.

See Also:
    `sympy`_, `symengine`_, and the compilation engine `numba`_

.. _sympy: http://docs.sympy.org/latest/index.html
.. _symengine: https://github.com/symengine/symengine
.. _numba: http://numba.pydata.org/
"""
import six
import numpy as np
import sympy as sy
import numba as nb
from platform import system
from sympy.utilities.lambdify import NUMPY_TRANSLATIONS, NUMPY_DEFAULT


npvars = vars(np)
npvars.update(NUMPY_DEFAULT)
npvars.update({k: getattr(np, v) for k, v in NUMPY_TRANSLATIONS.items()})
if "linux" in system().lower():
    jitkwargs = dict(nopython=True, nogil=True, parallel=True)
    veckwargs = dict(nopython=True, target="parallel")
else:
    jitkwargs = dict(nopython=True, nogil=True, parallel=False, cache=True)
    veckwargs = dict(nopython=True, target="cpu")


def numbafy(fn, args, compiler="jit", **nbkws):
    """
    Compile a string, sympy expression or symengine expression using numba.

    Note:
        Not all functions are supported by Python's numerical package (numpy).
        For difficult cases, valid Python code (as string) may be more suitable
        than symbolic expressions coming from sympy, symengine, etc.

    Args:
        fn: Symbolic expression as sympy/symengine expression or string
        args (iterable): Symbolic arguments
        compiler: String name or callable numba compiler
        nbkws: Compiler keyword arguments (if none provided, smart defaults are used)

    Returns:
        func: Compiled function

    Warning:
        The argument **nbkws** will override default options. The **cache**
        keyword argument is not guaranteed to be respected, especially when
        working in a dynamic/command line environment.
    """
    kwargs = {}    # Numba kwargs to be updated by user
    if not isinstance(args, (tuple, list)):
        args = (args, )
    # Parameterize compiler
    if isinstance(compiler, six.string_types):
        compiler_ = getattr(nb, compiler, None)
        if compiler is None:
            raise AttributeError("No numba function with name {}.".format(compiler))
        compiler = compiler_
    if compiler in (nb.jit, nb.njit, nb.autojit):
        kwargs.update(jitkwargs)
    else:
        kwargs.update(veckwargs)
    kwargs.update(nbkws)
    # Expand sympy expressions and create string for eval
    if isinstance(fn, sy.Expr):
        fn = sy.expand_func(fn)
    lamstr = "lambda " + ", ".join([str(a) for a in args]) + ": " + str(fn)
    # Python eval and docs
    func = eval(lamstr, npvars)
    func.__doc__ = "Dynamically compiled function:\n\n{}\n".format(lamstr)
    # Machine code compilation
    try:
        func = compiler(**kwargs)(func)
    except RuntimeError:
        kwargs.pop("cache")
        func = compiler(**kwargs)(func)
    # Add documentation/signature
    import warnings
    warnings.warn(lamstr)
    return func
