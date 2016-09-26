# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Function Compilation
##################################
Translation between the arguments used for :func:`~exa.compute.dispatch.dispatch`
-ing functions as well as compiling them for faster execution and parallelization.

See Also:
    Often times, compiling individual functions can be sped up via the
    :mod:`~exa.compute.dispatch` module.
"""
from exa._config import config
compilers = dict()
if config['dynamic']['numba']:
    pass
    #from exa.compute.compilers.nb import compiler as nb_compiler
    #compilers['numba'] = nb_compiler
compilers['default'] = nb_compiler if 'numba' in compilers else None


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

    The operators are "+" (AND), "|" (OR), "*", (propagate AND).

    | cpu: Compute only on CPU resources
    | gpu: Compute only on GPU resource
    | cpu+gpu: Computation on both CPU and GPU resources simultaneously
    | cpu|gpu: Compile signatures for cpu only and gpu only computation
    | (cpu|gpu)*mic: Compile signatures "cpu+mic|gpu+mic", but not "cpu+gpu+mic"
    | cpu*gpu*mic: Compile signatures for cpu only, gpu only, cpu+gpu, cpu+mic, gpu+mic, and cpu+gpu+mic computation

    The operator "+" acts to require all types of resources to be present, e.g.
    "cpu+gpu" requires a node with gpu compute capability, "cpu|gpu" functions
    can operate on a node that does or does not have a GPU, and "gpu" functions
    only operate on nodes that have gpu compute capability.

     Similarly, writing
    "cpu,gpu" will compile two function signatures one for operation on cpus
    only and one for operation on gpus only. For full cross compilation,
    "cpu:gpu" will create function signatures that will work on either only
    cpus, only gpus, or any combination therein. This can be extended to three
    resource objects as follows: "cpu+gpu:mic"

    Args:
        itypes (tuple): Input argument types
        otypes (tuple): Output type(s)
        contraction (str): Layout or dimensionality reduction/expansion
        processing (str): Choice of "cpu", "gpu", "mic" (e.g. "cpu+gpu")
        memory (str): Choice of "ram", "disk" (e.g. "ram|disk")
        parallelism (str): Choice of "none", "gilfree", "first", "second"
    """
    otypes = ("*", ) if otypes is None else otypes
    if compilers['default'] is None:
        return ("cpu", "ram", "none", ) + itypes, func
    elif compiler in compilers:
        return compilers[compiler](func, itypes, flags)
    raise KeyError("No such compiler {} available.".format(compiler))
