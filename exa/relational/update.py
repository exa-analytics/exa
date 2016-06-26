# -*- coding: utf-8 -*-
'''
Update Relational Tables
===============================================
Functions to facilitate updating relational tables.
'''
from exa.relational.base import engine
from exa.relational.unit import (Length, Mass, Time, Current, Amount,
                                 Luminosity, Dose, Acceleration,
                                 Charge, Dipole, Energy, Force,
                                 Frequency, MolarMass)
from exa.relational.isotope import Isotope
from exa.relational.constant import Constant


def drop_all_static_tables():
    '''
    Deletes all static (unit, isotope, and constant) tables.
    '''
    drop_units()
    drop_isotopes()
    drop_constants()


def drop_units():
    '''
    Drop all unit tables.
    '''
    Length.__table__.drop(engine)
    Mass.__table__.drop(engine)
    Time.__table__.drop(engine)
    Current.__table__.drop(engine)
    Amount.__table__.drop(engine)
    Luminosity.__table__.drop(engine)
    Dose.__table__.drop(engine)
    Acceleration.__table__.drop(engine)
    Charge.__table__.drop(engine)
    Dipole.__table__.drop(engine)
    Energy.__table__.drop(engine)
    Force.__table__.drop(engine)
    Frequency.__table__.drop(engine)
    MolarMass.__table__.drop(engine)


def drop_isotopes():
    '''
    Drop the isotopes table.
    '''
    Isotope.__table__.drop(engine)


def drop_constants():
    '''
    Drop the constants table.
    '''
    Constant.__table__.drop(engine)
