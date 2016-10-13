# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Computational Resources
########################
This module provides classes that describe how exa organizes computational
resources. Exa itself does not manage these resources, rather it keeps track of
them in order to quickly enable the :class:`~exa.compute.dispatch.Dispatcher` to
select the optimal function signature for a given set of inputs.
"""
import psutil
import numpy as np
from socket import gethostname


class Resource(object):
    """
    A computing resource ("node").

    Args:
        name (str): System alias or hostname
        loc (str): Typically the network address
        cpus (int): Number of CPU cores
        memory (int): Available RAM (bytes)
        gpus (int): Number of compute GPUs available
        disk (int): Amount of disk space available (bytes)
        scratch (str): Location on disk for scratch storage
        permanent (str): Location on disk for permanent storage
    """
    def __init__(self, name=None, location="localhost", cpus=4, memory=4000, gpus=0,
                 scratch=None, permanent=None, scratch_space=np.inf,
                 permanent_space=np.inf):
        self.name = gethostname() if name is None else str(name)
        self.location = location
        self.cpus = cpus
        self.memory = memory
        self.gpus = gpus
        self.scratch = scratch
        self.scratch_space = scratch_space
        self.permanent = permanent
        self.permanent_space = permanent_space

    def __repr__(self):
        clsname = self.__class__.__name__
        name = self.name
        cpus = str(self.cpus)
        gpus = str(self.gpus)
        mem = str(np.round(self.memory/1024**3))    # RAM in GB
        rep = "{}('{}', {} CPU, {} GPU, {} RAM)"
        return rep.format(clsname, name, cpus, gpus, mem)


class Resources(object):
    """A collection of :class:`~exa.compute.resources.Resource` objects."""
    @property
    def total_memory(self):
        """Get the total memory (bytes) available across all resources."""
        return sum(resource.memory for resource in self.resources)

    def __len__(self):
        return len(self.resources)

    def __init__(self, *resources):
        self.resources = resources


def get_ngpus():
    """Get the number of gpus present."""
    try:
        from numba import cuda
        return len(cuda.devices.gpus)
    except (AttributeError, ImportError):
        return 0


def inspect_resource(name=None, location="localhost"):
    """
    Get the parameters of a local or remote compute resource.

    Args:
        name (str): Common identifier for the resource
        location (str): Location of the resource (e.g. hostname or IP address)

    Returns:
        resource (:class:`~exa.compute.resources.Resource`): Inspected resource
    """
    def inspector():
        """Helper function to obtain the parameters of the resource."""
        cpus = psutil.cpu_count()
        memory = psutil.virtual_memory().total
        gpus = get_ngpus()
        return (cpus, memory, gpus)

    if location in ["localhost", "127.0.0.1"]:
        return Resource(name, location, *inspector())
    raise NotImplementedError("Need to implement connect.py first")


def default_resources(name=None):
    """Default resources are comprised of the local machine only."""
    return Resources(inspect_resource("default"))


def parallelize():
    """
    Decorator that automatically parallelizes GIL free functions within the
    "resources" framework provided by :mod:`~exa.compute.resources`
    """
    raise NotImplementedError()
