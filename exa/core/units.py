# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Quantity Support
#########################
Exa has a concept for a quantity, a number with associated units. This is
accomplished by leveraging Sympy's `unitsystem`_ interface. Quantities can be
used to define a single value or attached to data objects (such as a
:class:`~exa.core.discrete.Series` or :class:`~exa.core.discrete.DataFrame`).

.. _unitsystem: http://docs.sympy.org/dev/modules/physics/unitsystems/units.html
"""
