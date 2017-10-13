# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Physical Constants
#######################################
"""
from .quantity import FloatQuantity
from .units import si


class Constant(FloatQuantity):
    """
    """
    pass


c = Constant(299792458, si.velocity, "speed of light", "speed of light in vacuum")
G = Constant(6.67408E-11, si.force*si.velocity**2, "gravitational constant", "Newtonian constant of gravitation")
h = Constant(6.626070040E-34, si.energy*si.time, "Planck constant")
hbar = Constant(1.054571800E-34, si.energy*si.time, "reduced Planck constant")
