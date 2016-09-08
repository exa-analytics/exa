# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Relational
####################
This (sub)package is provides the content management framework for container
objects and a collection of static data for reference and unit conversions.
"""
#import atexit
#import pandas as pd
#from itertools import product
#from exa._config import config, del_update
#from exa.utility import mkp
#from exa.relational.base import engine, Base, scoped_session, session_factory
from exa.relational.unit import (Length, Mass, Time, Current, Amount, Luminosity,
                                 Dose, Acceleration, Charge, Dipole, Energy, Force,
                                 Frequency, MolarMass)
from exa.relational.isotope import Isotope
from exa.relational.constant import Constant
from exa.relational.project import Project
from exa.relational.job import Job
from exa.relational.file import DataFile, ContainerFile
#from exa.relational import test
#
#
## Static data loaders and table configuration (see below) are performed here
## because we import all of the table schemas here.
#def load_isotope_data():
#    """Load isotope data into the database (replacing existing)."""
#    path = mkp(config['dynamic']['pkgdir'], '..', "data", 'isotopes.json')
#    df = pd.read_json(path, orient='values')
#    df.columns = ('A', 'Z', 'af', 'eaf', 'color', 'radius', 'gfactor', 'mass',
#                  'emass', 'name', 'eneg', 'quadmom', 'spin', 'symbol', 'szuid',
#                  'strid')
#    df.index.names = ['pkid']
#    df.reset_index(inplace=True)
#    df.to_sql(name='isotope', con=engine, index=False, if_exists='replace')
#
#
#def load_unit_data():
#    """
#    Load unit conversions into the database (replacing existing).
#
#    Note:
#        This function actually computes (prior to bulk inserting data)
#        conversion factors.
#    """
#    path = mkp(config['dynamic']['pkgdir'], '..', 'data', 'units.json')
#    df = pd.read_json(path)
#    for column in df.columns:
#        series = df[column].dropna()
#        values = series.values
#        labels = series.index
#        n = len(values)
#        factor = (values.reshape(1, n) / values.reshape(n, 1)).ravel()
#        from_unit, to_unit = zip(*product(labels, labels))
#        df_to_save = pd.DataFrame.from_dict({'from_unit': from_unit,
#                                             'to_unit': to_unit,
#                                             'factor': factor})
#        df_to_save['pkid'] = df_to_save.index
#        df_to_save.to_sql(name=column, con=engine, index=False, if_exists='replace')
#
#
#def load_constant_data():
#    """Load constants into the database (replacing existing)."""
#    path = mkp(config['dynamic']['pkgdir'], '..', 'data', 'constants.json')
#    df = pd.read_json(path)
#    df.reset_index(inplace=True)
#    df.columns = ['symbol', 'value']
#    df['pkid'] = df.index
#    df.to_sql(name='constant', con=engine, index=False, if_exists='replace')
#
#
## Create tables if necessary and load static data (also if necessary)
## Note that relationship tables (e.g. projectjob in exa.relational.project)
## will be created automatically (without explicit import here).
#Base.metadata.create_all(engine)
#if config['db']['update'] == '1':
#    load_isotope_data()
#    load_unit_data()
#    load_constant_data()
#    atexit.register(del_update)
#
