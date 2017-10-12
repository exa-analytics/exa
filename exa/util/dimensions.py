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
import numpy as np
import pandas as pd
from exa import Typed, TypedClass, DataSeries
from exa.typed import yield_typed


empty_set = u"\u2205"
fundamentals = {'length': "L", 'temperature': "Θ", 'mass': "M", 'time': "T",
                'current': "I", 'amount': "N", 'luminosity': "J"}
empty_set_array = DataSeries(index=list(fundamentals.keys()))
empty_set_array.fillna(0, inplace=True)
empty_set_array = empty_set_array.astype(int).sort_index()


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

    def to_dict(self):
        return self.array.to_dict()

#    def decompose(self):
#        return tuple(sorted(self._symbols[k]+"^"+str(v) for k, v in self.to_dict().items() if v != 0))
#
#    def _as_array(self):
#        v = [self.length, self.mass, self.time, self.current,
#             self.temperature, self.amount, self.luminosity]
#        i = ['length', 'mass', 'time', 'current', 'temperature',
#             'amount', "luminosity"]
#        self.array = DataSeries(v, index=i, dtype=int).sort_index()

    def __eq__(self, other):
        """Equality checks each labeled unit."""
        if isinstance(other, Dimensions):
            return np.all(self.array == other.array)
        elif isinstance(other, pd.Series):
            return np.all(self.array == other)
        return False

    def __add__(self, other):
        """Addition/subtraction checks for equality."""
        if self == other:
            return self
        else:
            raise DimensionsError("Dimensions must match! Expected {}, got {}".format(self, other))

    def __mul__(self, other):
        """Multiplication is addition of powers."""
        if isinstance(other, Dimensions):
            array = self.array + other.array
            return Dimensions(**array.to_dict())
        return self

    def __truediv__(self, other):
        """Division is subtraction of powers."""
        if isinstance(other, Dimensions):
            array = self.array - other.array
            return Dimensions(**array.to_dict())
        else:
            return self**-1

    def __pow__(self, other):
        """Exponentiation is multiplication."""
        array = self.array*abs(other)
        if other < 0:
            return Dimensions(**(-array).to_dict())
        return Dimensions(**array.to_dict())

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __div__(self, other):
        return self.__truediv__(other)

    def __rdiv__(self, other):
        return self.__truediv__(other)

    def __sub__(self, other):
        return self.__add__(other)    # Subtraction is the same check as addition

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, length=0, mass=0, time=0, current=0, temperature=0,
                 amount=0, luminosity=0):
        self.array = DataSeries({'length': length, 'mass': mass, 'time': time,
                                 'current': current, 'temperature': temperature,
                                 'amount': amount, 'luminosity': luminosity},
                                dtype=int).sort_index()

    def __repr__(self):
        if self.array.abs().sum() == 0:
            return empty_set
        arr = self.array[self.array != 0]
        symbol = arr.index.map(lambda x: fundamentals[x]).astype(str)
        power = arr.astype(str)
        return " ".join(sorted((symbol+"^"+power).tolist()))


# Base Dimensions
angle = Dimensions()
mass = Dimensions(mass=1)
length = Dimensions(length=1)
time = Dimensions(time=1)
current = Dimensions(current=1)
temperature = Dimensions(temperature=1)
amount = Dimensions(amount=1)
luminosity = Dimensions(luminosity=1)


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
