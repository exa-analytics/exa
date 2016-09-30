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

+------------------------+----------------------+----------------------------+
| processing             | memory               | parallelism                |
+========================+======================+============================+
| cpu, gpu               | ram, disk            | serial, gilfree, resources |
+------------------------+----------------------+----------------------------+

Combined with the input argument (and possibly output) type(s), a unique
signature can be created for each algorithm implementation. If alternative
function algorithms are not required for different types for parallization
schemes (for example), a new function is not compiled rather the previously
compiled function is referenced.

Processing described the object expected for perfoming computation. Memory
describes whether the function acts only in memory, or only (primarily) out of
core. Parallelism describes the type of parallelization (if available) the
function is capable of: serial - no parallelization, gilfree - no intrinsic
parallelization, but ready for embarassingly parallel applications i.e. the
function can be executed in parallel "by hand", and resources - local or
distributed parallelization using the exa resources scheme.

See Also:
    For a description of automatic function compilation, see
    :mod:`~exa.compute.dispatch`. Additional information regarding computational
    resources and workflows can be found in :mod:`~exa.compute.resource` and
    :mod:`~exa.compute.workflow`.
"""
from functools import wraps
from exa._config import config
from exa.compute.resource import default_resources
compilers = {'none': None}
if config['dynamic']['numba']:
    from exa.compute.compilers.nb import compiler as nb_compiler
    compilers['numba'] = nb_compiler


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


def resources_required():
    """
    Decorator used to inject a resource argument for intrinsically parallel
    functions.
    """
    def parallel_func(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            resources = kwargs.pop("resources", default_resources())
            return func(*args, **kwargs)
        return func
    return parallel_func


def static_otype(*otypes):
    """
    Decorator
    """
    def conv_func(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if len(otypes) == 1:
                return otypes[0](func(*args, **kwargs))
            return tuple([otypes[i](obj) for i, obj in enumerate(func(*args, **kwargs))])
        return func_wrapper
    return conv_func


def compile_function(func, itypes, compiler='none', otypes=None):
    """
    Compile a function using a specified backend compiler.

    .. code-block:: Python

        from numbers import Real

        def fn(a, b, c):
            d = a*b
            return "ans: {}, {}".format(str(d), c)

        itypes = (Real, Real, str)
        sig, fnc = compile_function(fn, itypes)

    Args:
        itypes (tuple): Tuple of argument types
        compiler (str): See :func:`~exa.compute.compilers.wrapper.available_compilers`
        otypes (tuple): Tuple of output type(s) or None
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



    Compilation accepts a number of human readable arguments. To compile a
    function that requires both CPU and GPU resources, acts in memory only,
    and supports single node and multinode parallelization, the following
    arguments would work:

    .. code-block:: Python

        compile_function(func, itypes, processing="cpu+gpu", memory="ram",
                         processing="first,second")
        # Alternatively...
        @dispatch(*itypes, processing="cpu+gpu", memory="ram", processing="first,second")
        def func(arg0, ...):
            ...

    The operators are "+" (AND), "\|" (OR), "*", (propagate).

    | cpu: Compute only on CPU resources
    | gpu: Compute only on GPU resource
    | cpu+gpu: Computation on both CPU and GPU resources simultaneously
    | cpu|gpu: Compile signatures for cpu only and gpu only computation
    | (cpu|gpu)*mic: Compile signatures "cpu+mic|gpu+mic", but not "cpu+gpu+mic"
    | cpu*gpu*mic: Compile signatures for cpu only, gpu only, cpu+gpu, cpu+mic, gpu+mic, and cpu+gpu+mic computation

    Args:
        itypes (tuple): Input argument types
        otypes (tuple): Output type(s)
        contraction (str): Layout or dimensionality reduction/expansion
        processing (str): Choice of "cpu", "gpu", "mic" (e.g. "cpu+gpu")
        memory (str): Choice of "ram", "disk" (e.g. "ram|disk")
        parallelism (str): Choice of "none", "gilfree", "first", "second"
    """
    try:
        compiler = compilers[compiler]
    except KeyError:
        raise KeyError("No such compiler {} available.".format(compiler))
    if compiler is None:
        return ("cpu", "ram", "serial", ) + itypes, func
    else:
        return compilers[compiler](func, itypes, flags)
