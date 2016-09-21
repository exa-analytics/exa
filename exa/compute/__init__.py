# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This sub-package contains functionality for performing computation.

- :class:`~exa.compute.resource.Resources`: A representation of external computing resources
- :class:`~exa.compute.workflow.Workflow`: Programmatic computation
- :class:`~exa.compute.dispatch.Dispatcher`: Multiple dispatch, compilation, and parallelization
- :class:`~exa.compute.conectivity.SSH`: Inter node communication for workflows
"""
# Import modules
from exa.compute import dispatch

# Import sub-packages
from exa.compute import tests

# Import user/dev API
