# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Unit Systems
####################################
"""
from sympy.physics.unitsystems import units


class Unit(units.Unit):
    """
    """
    @classmethod
    def from_sympy(cls, unit, abbrev=None):
        if abbrev is None:
            return cls(unit.dim, abbrev=unit.abbrev, factor=unit.factor)
        return cls(unit.dim, abbrev=abbrev, factor=unit.factor)

    def _constructor(self, unit, abbrev):
        return self.from_sympy(unit, abbrev)

    def __pow__(self, power):
        abbrev = self.abbrev + "^" + str(power)
        obj = self.pow(power)
        return self._constructor(obj, abbrev)


# Base units
meter = Unit(length, factor=1, abbrev="m")
kilogram = Unit(mass, factor=1000, abbrev="g", prefix=prefixes.PREFIXES["k"])
second = Unit(time, abbrev="s", factor=1)
candela = Unit(luminosity, abbrev="cd", factor=1)
mole = Unit(amount, abbrev="mol", factor=1)
kelvin = Unit(temperature, abbrev="K", factor=1)
ampere = Unit(current, abbrev="A", factor=1)
