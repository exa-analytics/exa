# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Function Compilation
##################################
Translation between the arguments used for :func:`~exa.compute.dispatch.dispatch`
-ing functions as well as compiling them for faster execution and parallelization.

+----------------+------+----------+--------+--------+
| category/index |  0   |   1      |  2     | 3      |
+================+======+==========+========+========+
| processing     | cpu  | gpu      | mic    |        |
+----------------+------+----------+--------+--------+
| memory         | ram  | disk     |        |        |
+----------------+------+----------+--------+--------+
| parallelism    | none | gilfree  | first  | second |
+----------------+------+----------+--------+--------+
| first: single node, multithread/multiprocess       |
+----------------------------------------------------+
| second: multi node, multithread/multiprocess       |
+----------------------------------------------------+

Functions that get compiled with "first" or "second" parallelism will
automatically obtain machinery to handle a resource kwarg.

See Also:
    Often times, compiling individual functions can be sped up via the
    :mod:`~exa.compute.dispatch` module.
"""
from exa._config import config
compilers = {'none': None}
if config['dynamic']['numba']:
    pass
    from exa.compute.compilers.nb import compiler as nb_compiler
    compilers['numba'] = nb_compiler
compilers['default'] = compilers['numba'] if 'numba' in compilers else None


def available_compilers():
    """Display available compilers."""
    return compilers.keys()


def compile_function(func, itypes, compiler='default', otypes=None):
    """
    Compile a function using a specified compiler.

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
        return (0, 0, 0, ) + itypes, func
    else:
        return compilers[compiler](func, itypes, flags)
