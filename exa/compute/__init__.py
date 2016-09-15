# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Computation
######################
This sub-package contains all compuation related features of the exa framework:

- :class:`~exa.compute.resource.Resources`: A representation of external computing resources
- :class:`~exa.compute.workflow.Workflow`: Programmatic computation
- :class:`~exa.compute.dispatch.Dispatcher`: Multiple dispatch, compilation, and parallelization
- :class:`~exa.compute.conectivity.SSH`: Inter node communication for workflows
"""
from exa.compute import dispatch
from exa.compute import workflow
