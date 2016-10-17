# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Function Compilation
##################################
This module provides a generic wrapper for different compilation machinery
available in the Python ecosystem. It provides a systematic API for developers
writing compiled functions which is compiler backend independent. In this way
the same algorithm can be tested with a number of different compiler backends
without needing to be rewritten. The human readable categories for describing
compiled functions are as follows.

To compile for multiple targets simultaneously use "|", e.g. "cpu|gpu". If the
function requires multiple target resources use "+", e.g. "cpu+gpu".

+--------+--------------+------------------------------------------------------+
| name   | description  | values                                               |
+========+==============+======================================================+
| target | processor(s) | cpu, gpu                                             |
+--------+--------------+------------------------------------------------------+
| core   | memory use   | ram, disk                                            |
+--------+--------------+------------------------------------------------------+
| mp     | compilation  | serial, unroll, vec, gvec, parallel, distrib         |
+--------+--------------+------------------------------------------------------+

The **ftype** argument describes the compilation strategy to be used. When using
**unroll**, compilation expands loops and reduces all operations to primitive
operations. Likewise, **vec** transforms a `ufunc`_ into a vectorized operation,
an operation that can be quickly applied to all elements of an array. The option
**gvec** generalizes **vec** to act on multidimensional arguments.

The **target** argument describes the type of processing unit (or units) to be
used. Examples are **cpu** and **gpu**.

The **core** argument describes whether the algorithm supports out of core
processing (**disk**) or not (**ram**).

The **mp** argument describes the compilation and (possible) parallelization
strategy for the function. Serial functions (**serial**) are not parallelized
and are `GIL`_ locked. `GIL`_ free functions (that can additionally be used in
embarassingly parallel execution) Functions compiled with the **nogil** flag are not intrinsically parallelized
but support parallel execution because they release the `GIL`_. Intrinsically
parallel functions come in two flavors, **parallel** and **distrib**. The
former type refers to functions that are parallelized for shared memory,
symmetric multiprocessing architectures (single node). The latter type refers
to those functions parallelized for distributed computing systems (it is common
to develop a "parallel" function that then can be wrapped by a "distributed"
function).

See Also:
    For a description of automatic function compilation, see
    :mod:`~exa.compute.dispatch`. Additional information regarding computational
    resources and workflows can be found in :mod:`~exa.compute.resource` and
    :mod:`~exa.compute.workflow`.

.. _GIL: https://wiki.python.org/moin/GlobalInterpreterLock
.. _ufunc: https://docs.scipy.org/doc/numpy/reference/ufuncs.html
"""
from functools import wraps
from exa._config import config
compilers = {'none': None}
if config['dynamic']['numba'] == "true":
    from exa.compute.compilers.nb import compiler as nb_compiler
    compilers['numba'] = nb_compiler
if config['dynamic']['cython'] == "true":
    from exa.compute.compilers.cy import compiler as cy_compiler
    compilers['cython'] = cy_compiler
if 'numba' in compilers:
    default_compiler = 'numba'
elif 'cython' in compilers:
    default_compiler = 'cython'
else:
    default_compiler = 'none'


def available_compilers():
    """Display available compilers."""
    return compilers.keys()


def check_memerr():
    """
    Decorator to check the function for a possible memory error based on the
    function's memory complexity and size of input arguments.
    """
    pass


def check_diskerr():
    """
    Decorator to check for possible disk usage error given the function's disk
    usage complexity and arguments.
    """
    pass


def returns(*otypes):
    """
    Decorator that attempts to convert function outputs to specified types.

    By default, if conversion fails, the unconverted result is passed through.

    Args:
        otypes (tuple): Output type(s)

    Returns:
        func (function): Wrapped function

    Raises:
        TypeError: On failed conversion
    """
    def conv_func(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if len(otypes) == 0:
                return func(*args, **kwargs)
            elif len(otypes) == 1:
                return otypes[0](func(*args, **kwargs))
            return tuple([otypes[i](obj) for i, obj in enumerate(func(*args, **kwargs))])
        return func_wrapper
    return conv_func


def compile_function(func, *itypes, **flags):
    """
    Compile a function using a specified backend compiler.

    Args:
        itypes (tuple): Tuple of argument types
        otypes (tuple): Tuple of output type(s) or None
        compiler (str): See :func:`~exa.compute.compilers.wrapper.available_compilers`
        nosig (bool): Don't return signature (default false)
        target (str): Computing target "cpu", "gpu"
        core (str): One, or combination of "ram", "disk"
        mp (str): One, or combination of "serial", "gilfree", "resources"

    Returns:
        sig, func: Tuple of function signature (tuple) and compiled function (function)
    """
    compiler = flags.pop("compiler", "none")
    nosig = flags.pop("nosig", False)
    try:
        compiler = compilers[compiler]
    except KeyError:
        raise KeyError("No such compiler {} available.".format(compiler))
    if compiler is None:
        sig = ("cpu", "ram", "serial", ) + itypes
    else:
        sig, func = compiler(func, *itypes, **flags)
    if nosig:
        return func
    return sig, func
