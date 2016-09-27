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
import numpy as np


class Resource(object):
    """
    A computing resource ("node").

    Args:
        name (str): System alias or hostname
        loc (str): Typically the network address
        tasks (int): Number of CPU cores
        mem (int): Available RAM
        gpu (int): Number of compute GPUs available
        mic (int): Number of compute MICs available
        disk (int): Amount of disk space available
        scratch (str): Location of disk scratch/temporary space
    """
    def __init__(self, name, loc, tasks=4, mem=4000, gpu=0, mic=0, disk=np.inf,
                 scratch=None):
        self.name = name
        self.loc = loc
        self.tasks = tasks
        self.mem = mem
        self.gpu = gpu
        self.mic = mic
        self.disk = disk
        self.scratch = scratch


class ComputeResources(object):
    """A collection of :class:`~exa.compute.resource.Resource` objects."""
    @property
    def total_memory(self):
        """Get the total memory available across all resources."""
        return sum(resource.mem for resource in self.resources)

    def __init__(self, *resources):
        self.resources = resources


def collect_resources():
    pass
