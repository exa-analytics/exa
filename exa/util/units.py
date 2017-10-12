# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Units and Unit Systems
############################
The :class:`~exa.util.units.Unit` is a :class:`~exa.util.dimensions.Dimension`
that has a name.
"""
from . import dimensions
from .dimensions import Dimensions, fundamentals
from exa import Typed, TypedClass



prefix2sym = {'yotta': "Y", 'zetta': "Z", 'exa': "E", 'tera': "T",
              'giga': "G", 'mega': "M", 'kilo': "k", 'hecto': "h",
              'deka': "da", 'deci': "d", 'centi': "c", 'milli': "m",
              'micro': "µ", 'nano': "n", 'pico': "p", 'femto': "f",
              'atto': "a", 'zepto': "z", 'yocto': "y"}
sym2fac = {'Y': 1E24, 'Z': 1E21, 'E': 1E18, 'P': 1E15, 'T': 1E12, 'G': 1E9,
           'M': 1E6, 'k': 1E3, 'h': 1E2, 'da': 1E1, 'd': 1E-1, 'c': 1E-2,
           'm': 1E-3, 'µ': 1E-6, 'n': 1E-9, 'p': 1E-12, 'f': 1E-15, 'a': 1E-18,
           'z': 1E-21, 'y': 1E-24}
sym2prefix = {v: k for k, v in prefix2sym.items()}
fac2sym = {v: k for k, v in sym2fac.items()}


class UnitError(Exception):
    """Raised when unit math operations fail."""
    pass


class Unit(Dimensions):
    """A unit is a named dimension object."""
    @property
    def name(self):
        """Falls back to dimensions."""
        if self._suffix is None:
            return super(Unit, self).__repr__()
        return self._prefix + self._suffix

    @property
    def symbol(self):
        """Falls back to full name."""
        if self._symbol is None:
            return self.name
        return prefix2sym.get(self._prefix, "") + self._symbol

    @property
    def _constructor(self):
        return Unit

    def __init__(self, fullname=None, symbol=None, prefix=None, **dimensions):
        super(Unit, self).__init__(**dimensions)
        # Determine "base" name and prefix
        self._suffix = None    # Full by default
        self._prefix = None    # Full by default
        self._symbol = symbol
        # Figure out the suffix and prefix
        if fullname is None:
            self._suffix = fullname
        else:
            for pref in prefix2sym.keys():
                if fullname.startswith(pref):
                    self._suffix = fullname.replace(pref, "", 1)
                    self._prefix = pref
                    if symbol is not None:
                        prf = prefix2sym[pref]
                        if symbol.startswith(prf):
                            self._symbol = symbol.replace(prf, "", 1)
                        else:
                            self._symbol = symbol
                    break
            else:
                if prefix is None:    # Understand the fullname to be the suffix
                    self._prefix = ""
                elif prefix in prefix2sym:
                    self._prefix = prefix
                elif prefix in sym2prefix:
                    self._prefix = sym2prefix[prefix]
                else:
                    raise UnitError("Invalid prefix {}".format(prefix))
                self._suffix = fullname

    def __repr__(self):
        return self.symbol


def Quantity(TypedClass):
    """
    A number with units.
    """
    value = Typed(float)
    unit = Typed(Unit)

    def __add__(self, other):
        if isinstance(other, Quantity) and self.unit == other.unit:
            pass


    def __init__(self, value, unit):
        self.value = value
        self.unit = unit


class UnitSystem(TypedClass):
    """A system of unit objects from which all other units can be derived."""
    length = Typed(Unit)
    mass = Typed(Unit)
    time = Typed(Unit)
    current = Typed(Unit)
    temperature = Typed(Unit)
    amount = Typed(Unit)
    luminosity = Typed(Unit)

    def base(self, full=False):
        """Return base units."""
        base = {'length': self.length, 'mass': self.mass, 'time': self.time,
                'temperature': self.temperature, 'current': self.current,
                'amount': self.amount, 'luminosity': self.luminosity}
        if full == True:
            return base
        return {k: v for k, v in base.items() if v is not None}

    def _derived_units(self):
        """Generate derived units."""
        base = self.base()
        for k, v in vars(dimensions).items():
            if isinstance(v, Dimensions) and k not in fundamentals:
                derived = None
                symbol = []
                for dim, exp in v.array.items():
                    if exp == 0:
                        continue
                    if dim not in base:
                        derived = None
                        break
                    else:
                        unit = base[dim]
                        if derived is None:
                            derived = unit**exp
                        else:
                            derived *= unit**exp
                        if exp != 0:
                            symbol.append(str(unit.symbol) + "^" + str(exp))
                if derived is not None:
                    symbol = " ".join(sorted(symbol))
                    derived = Unit(symbol=symbol, **derived.array.to_dict())
                    setattr(self, k, derived)

    def __init__(self, name=None, length=None, mass=None, time=None, current=None,
                 temperature=None, amount=None, luminosity=None):
        self.length = length
        self.mass = mass
        self.time = time
        self.current = current
        self.temperature = temperature
        self.amount = amount
        self.luminosity = luminosity
        self.name = name
        self._derived_units()

    def __repr__(self):
        baserepr = ", ".join([str(k)+": "+str(v) for k, v in self.base().items()])
        if self.name:
            return "{}({})".format(self.name, baserepr)
        return "UnitSystem({})".format(baserepr)






#    @property
#    def name(self):
#        if self._suffix is None:
#            return self._dimensions
#        return self._prefix + self._suffix
#
#    @property
#    def symbol(self):
#        if self._symbol is None:
#            return self.name
#        return self._name2sym.get(self._prefix, "") + self._symbol
#
#    def __add__(self, other):
#        if isinstance(other, Unit):
#            dims = self._dimensions + other._dimensions
#        else:
#            raise UnitError("How does 1?")
#        return Unit(fullname="derived", **dims.to_dict())
#
#    def __sub__(self, other):
#        if isinstance(other, Unit):
#            dims = self._dimensions - other._dimensions
#        else:
#            raise UnitError("How does 2?")
#        return Unit(fullname="derived", **dims.to_dict())
#
#    def __radd__(self, other):
#        return self.__add__(other)
#
#    def __rsub__(self, other):
#        return self.__sub__(other)
#
#    def __mul__(self, other):
#        if isinstance(other, Unit):
#            dims = self._dimensions*other._dimensions
#        else:
#            raise UnitError("How does 3?")
#        return Unit(fullname="derived", **dims.to_dict())
#
#    def __rmul__(self, other):
#        return self.__mul__(other)
#
#    def __div__(self, other):
#        if isinstance(other, Unit):
#            dims = self._dimensions/other._dimensions
#        else:
#            raise UnitError("How does 4?")
#        return Unit(fullname="derived", **dims.to_dict())
#
#    def __truediv__(self, other):
#        return self.__div__(other)
#
#    def __rdiv__(self, other):
#        return self.__div__(other)
#
#    def __rtruediv__(self, other):
#        return self.__div__(other)
#
#    def __pow__(self, other):
#        if isinstance(other, Unit):
#            raise UnitError("How does 5?")
#        dims = self._dimensions**other
#        return Unit(fullname="derived", **dims.to_dict())
#
#
#
#class Quantity(TypedClass):
#    """A number with units."""
#    value = Typed((int, float, np.int64, np.int32, np.float64, np.float32))
#    unit = Typed(Unit)
#
#    def __init__(self, value, unit):
#        self.value = value
#        self.unit = unit
#
#
#class TestUnit(TestCase):
#    def test_init(self):
#        kgstr = "kilogram"
#        unit = Unit("gram", prefix="kilo")
#        self.assertEqual(str(unit), kgstr)
#        unit = Unit("gram", symbol="g", prefix="k")
#        self.assertEqual(str(unit), "kg")
#        unit = Unit(kgstr)
#        self.assertEqual(str(unit), kgstr)
#        unit = Unit("gram", prefix="k")
#        self.assertEqual(str(unit), kgstr)
#
#
#TextTestRunner().run(TestLoader().loadTestsFromModule(TestUnit()))
#
#    def __repr__(self):
#        base = ", ".join([k+": "+str(v) for k, v in self.base_units().items()]).strip()
#        if self.name is None:
#            return "UnitSystem({})".format(base)
#        return "{}({})".format(self.name, base)
#
#
#si = UnitSystem("SI", length=Unit("meter", "m"), time=Unit("second", "s")) #mass=Unit("kilogram", "kg"))
#si
#
#
#_bu_map = {'length': "L^1", 'mass': "M^1", 'time': "T^1", 'temperature': "Θ^1",
#           'current': "J^1", 'amount': "N^1", 'luminosity': "I^1"}
#def generate_unit(self, *args):
#    """Arguments follow the order dim0 op dim1 (op dim2 etc.)."""
#    baseunits = {_bu_map[k]: v for k, v in self.base_units().items()}
#    units = [baseunits.get(str(dim), None) for dim in args[::2]]
#    if None in units:
#        return
#    ops = args[1::2]
#    value = units.pop(0)
#    for i in range(len(units)):
#        value = getattr(value, ops[i])(units[i])
#    return value
