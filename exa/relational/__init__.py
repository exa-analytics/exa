# -*- coding: utf-8 -*-
import pandas as pd
from itertools import product
from exa._config import config
from exa.relational.unit import (Length, Mass, Time, Current, Amount,
                                 Luminosity, Dose, Acceleration,
                                 Charge, Dipole, Energy, Force,
                                 Frequency, MolarMass)
from exa.relational.isotope import Isotope, init_mappers
from exa.relational.constant import Constant
#
#from exa.relational.file import File
#from exa.relational.container import Container
from exa.container import BaseContainer as Container
#
from exa.relational import tests
from exa.relational.base import Base, create_db, cleanup_db
from exa.utility import mkp


def install_db(drop=False, verbose=False):
    '''
    Installs static data: database conversion tables and Jupyter notebook extensions

    Args:
        drop (bool): Drop static data before loading (required for persistent install)
        verbose (bool): Verbose notebook extension installation
    '''
    if 'engine' in config:
        cleanup_db()
    create_db()
    if drop == True:
        try:
            drop_all_static_tables()
        except:
            pass
    try:
        load_isotope_data()
    except:
        pass
    try:
        load_unit_data()
    except:
        pass
    try:
        load_constant_data()
    except:
        pass
    init_mappers()


def load_isotope_data():
    '''
    Load isotope data (from isotopes.json) into the database.
    '''
    df = pd.read_json(mkp(config['static'], 'isotopes.json'), orient='values')
    df.columns = ('A', 'Z', 'af', 'eaf', 'color', 'radius', 'gfactor', 'mass', 'emass',
                  'name', 'eneg', 'quadmom', 'spin', 'symbol', 'szuid', 'strid')
    df.index.names = ['pkid']
    df.reset_index(inplace=True)
    df.to_sql(name='isotope', con=config['engine'], index=False, if_exists='replace')


def load_unit_data():
    '''
    Load unit conversions (from units.json) into the database.
    '''
    df = pd.read_json(mkp(config['static'], 'units.json'))
    for column in df.columns:
        series = df[column].copy().dropna()
        values = series.values
        labels = series.index
        n = len(values)
        factor = (values.reshape(1, n) / values.reshape(n, 1)).ravel()
        from_unit, to_unit = list(zip(*product(labels, labels)))
        df_to_save = pd.DataFrame.from_dict({'from_unit': from_unit, 'to_unit': to_unit, 'factor': factor})
        df_to_save['pkid'] = df_to_save.index
        df_to_save.to_sql(name=column, con=config['engine'], index=False, if_exists='replace')


def load_constant_data():
    '''
    Load constants (from constants.json) into the database.
    '''
    df = pd.read_json(mkp(config['static'], 'constants.json'))
    df.reset_index(inplace=True)
    df.columns = ['symbol', 'value']
    df['pkid'] = df.index
    df.to_sql(name='constant', con=config['engine'], index=False, if_exists='replace')


def drop_all_static_tables():
    '''
    Deletes all static (unit, isotope, and constant) tables.
    '''
    Length.__table__.drop(config['engine'])
    Mass.__table__.drop(config['engine'])
    Time.__table__.drop(config['engine'])
    Current.__table__.drop(config['engine'])
    Amount.__table__.drop(config['engine'])
    Luminosity.__table__.drop(config['engine'])
    Dose.__table__.drop(config['engine'])
    Acceleration.__table__.drop(config['engine'])
    Charge.__table__.drop(config['engine'])
    Dipole.__table__.drop(config['engine'])
    Energy.__table__.drop(config['engine'])
    Force.__table__.drop(config['engine'])
    Frequency.__table__.drop(config['engine'])
    MolarMass.__table__.drop(config['engine'])
    Isotope.__table__.drop(config['engine'])
    Constant.__table__.drop(config['engine'])
