# -*- coding: utf-8 -*-
'''
exa.relational
####################
This (sub)package is provides the content management framework for container
objects and a collection of static data for reference and unit conversions.
'''
import pandas as pd
from exa._config import config
from exa.relational.base import engine, Base
from exa.relational.file import File
from exa.relational.unit import (Length, Mass, Time, Current, Amount, Luminosity,
                                 Dose, Acceleration, Charge, Dipole, Energy, Force,
                                 Frequency, MolarMass)
from exa.relational.isotope import Isotope
from exa.relational.constant import Constant


# Static data
def load_isotope_data():
    '''Load isotope data (from isotopes.json) into the database.'''
    df = pd.read_json(mkp(config['static'], 'isotopes.json'), orient='values')
    df.columns = ('A', 'Z', 'af', 'eaf', 'color', 'radius', 'gfactor', 'mass', 'emass',
                  'name', 'eneg', 'quadmom', 'spin', 'symbol', 'szuid', 'strid')
    df.index.names = ['pkid']
    df.reset_index(inplace=True)
    df.to_sql(name='isotope', con=engine, index=False, if_exists='replace')


def load_unit_data():
    '''Load unit conversions (from units.json) into the database.'''
    df = pd.read_json(mkp(config['static'], 'units.json'))
    for column in df.columns:
        series = df[column].copy().dropna()
        values = series.values
        labels = series.index
        n = len(values)
        factor = (values.reshape(1, n) / values.reshape(n, 1)).ravel()
        from_unit, to_unit = list(zip(*product(labels, labels)))
        df_to_save = pd.DataFrame.from_dict({'from_unit': from_unit,
                                             'to_unit': to_unit,
                                             'factor': factor})
        df_to_save['pkid'] = df_to_save.index
        df_to_save.to_sql(name=column, con=engine, index=False, if_exists='replace')


def load_constant_data():
    '''Load constants (from constants.json) into the database.'''
    df = pd.read_json(mkp(config['static'], 'constants.json'))
    df.reset_index(inplace=True)
    df.columns = ['symbol', 'value']
    df['pkid'] = df.index
    df.to_sql(name='constant', con=engine, index=False, if_exists='replace')


def drop_all_static_tables():
    '''Deletes all static (unit, isotope, and constant) tables.'''
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
    Isotope.__table__.drop(engine)
    Constant.__table__.drop(engine)


# Create tables if necessary and load static data (also if necessary)
Base.metadata.create_all(engine)
if config['db']['update'] == '1':
    drop_all_static_tables()
    load_isotope_data()
    load_unit_data()
    load_constant_data()
