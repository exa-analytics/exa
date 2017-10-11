# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Dimensions
#######################################
Mathematical operations between dimensions are different than for dimensionless
numbers. Dimensions are the basis of creating :class:`~exa.util.units.Unit`
objects.
"""
from exa import Typed, TypedClass, DataSeries
from exa.typed import yield_typed


symbols = {'length': "L", 'temperature': "Θ", 'mass': "M", 'time': "T",
           'current': "I", 'amount': "N", 'luminosity': "J"}


class DimensionsError(Exception):
    """Raised when dimensional math operations fail."""
    pass


class Dimensions(TypedClass):
    """
    A descriptor of dimensions associated with a physical action, quantity, or
    object.

    The possible fundamental dimensions are length (L), mass (M),
    temperature (Θ), time (T), current (I), amount (N), and luminosity
    (luminous intensity - J). The fundamental dimensions are stored as a
    labeled array. All math operations are performed on the underlying array.
    """
    _setters = ("_as", )
    length = Typed(int, allow_none=False)
    mass = Typed(int, allow_none=False)
    time = Typed(int, allow_none=False)
    current = Typed(int, allow_none=False)
    temperature = Typed(int, allow_none=False)
    amount = Typed(int, allow_none=False)
    luminosity = Typed(int, allow_none=False)
    array = Typed(DataSeries)

#    def to_dict(self):
#        return self.array.to_dict()
#
#    def decompose(self):
#        return tuple(sorted(self._symbols[k]+"^"+str(v) for k, v in self.to_dict().items() if v != 0))
#
#    def _as_array(self):
#        v = [self.length, self.mass, self.time, self.current,
#             self.temperature, self.amount, self.luminosity]
#        i = ['length', 'mass', 'time', 'current', 'temperature',
#             'amount', "luminosity"]
#        self.array = DataSeries(v, index=i, dtype=int).sort_index()

    def __add__(self, other):
        if isinstance(other, Dimensions) and np.all(other.array == self.array):
            return self
        else:
            raise DimensionsError("Dimensions must match! Expected {}, got {}".format(self, other))

    def __sub__(self, other):
        if isinstance(other, Dimensions) and np.all(other.array == self.array):
            return self
        else:
            raise DimensionsError("Dimensions must match! Expected {}, got {}".format(self, other))

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, Dimensions):
            array = self.array + other.array
        else:
            array = self.array*other
        return Dimensions(**array.to_dict())

    def __div__(self, other):
        if isinstance(other, Dimensions):
            array = self.array - other.array
        else:
            array = -self.array
        return Dimensions(**array.to_dict())

    def __truediv__(self, other):
        return self.__div__(other)

    def __rtruediv__(self, other):
        return self.__div__(other)

    def __rdiv__(self, other):
        return self.__div__(other)

    def __pow__(self, other):
        if isinstance(other, Dimensions) and other.array.abs().sum() > 0:
            raise DimensionsError("Exponentiation must be dimensionless (got {})!".fromat(other))
        elif other < 0:
            return self.__truediv__(other)
        else:
            return self.__mul__(other)

    def __init__(self, length=0, mass=0, time=0, current=0,
                 temperature=0, amount=0, luminosity=0):
        self.array = DataSeries({'length': length, 'mass': mass, 'time': time,
                                 'current': current, 'temperature': temperature,
                                 'amount': amount, 'luminosity': luminosity},
                                dtype=int)

    def __repr__(self):
        rep = []
        for measure in yield_typed(self):
            if measure not in ("array", ) and getattr(self, measure) != 0:
                rep.append(self._symbols[measure] + "^{}".format(getattr(self, measure)))
        if len(rep) == 0:
            return u"\u2205"
        return " ".join(rep).strip()
#
#
#
## Base Dimensions
#angle = Dimensions()
#mass = Dimensions(mass=1)
#length = Dimensions(length=1)
#time = Dimensions(time=1)
#current = Dimensions(current=1)
#temperature = Dimensions(temperature=1)
#amount = Dimensions(amount=1)
#luminosity = Dimensions(luminosity=1)
#
#
## Derived Dimensions
#area = length**2
#volume = length**3
#speed = velocity = length/time
#acceleration = speed/time
#jerk = acceleration/time
#wave_number = 1/length
#mass_density = mass/volume
#current_density = current/area
#magnetic_field_strength = current/length
#luminance = luminosity/area
#frequency = 1/time
#force = mass*length/time**2
#pressure = force/area
#energy = force*length
#power = energy/time
#electric_charge = current*time
#electric_potential = power/current
#capacitance = electric_charge/electric_potential
#electric_resistance = electric_potential/current
#electric_conductance = 1/electric_resistance
#magnetic_flux = electric_potential*time
#magnetic_flux_density = magnetic_flux/area
#inductance = magnetic_flux/current
#dose = energy/mass
#catalytic_activity = amount/time
#
## Additional derived
#dynamic_viscosity = pressure*time
#moment_of_force = force*length
#surface_tension = force/length
#angular_velocity = angle/time
#angular_acceleration = angle/time**2
#irradiance = power/area
#heat_capacity = energy/temperature
#specific_heat_capacity = energy/temperature/mass
#specific_energy = energy/mass
#thermal_conductivity = power/length/temperature
#energy_density = energy/volume
#electric_field_strength = electric_potential/length
#electric_charge_density = electric_charge/volume
#electric_charge_flux = electric_charge/area
#permittivity = capacitance/length
#permeability = inductance/length
#molar_energy = energy/amount
#molar_heat_capacity = energy/temperature/amount
#exposure = electric_charge/mass
#dose_rate = dose/time
#radiant_intensity = power/angle
#radiance = radiant_intensity/area
#catalytic_concentration = catalytic_activity/volume
