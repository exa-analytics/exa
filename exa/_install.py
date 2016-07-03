# -*- coding: utf-8 -*-
'''
Installer
########################
This module allows a user to install exa in a persistent manner enabling some
advanced content management features. Installation will create a permanent
directory where exa's relational database will be housed (default ~/.exa).
All container creation, logging, and static data is housed in this directory.

See Also:
    :mod:`~exa._config`
'''
import os
import shutil
import platform
import pandas as pd
from itertools import product
from notebook import install_nbextension
from exa._config import update_config, save_config, config
from exa._config import cleanup as config_cleanup
from exa.log import setup_loggers
from exa.utility import mkp


def install(persist=False, verbose=False):
    '''
    Sets up the database and Jupyter notebook extensions. If install with
    persistence, will perform setup in the "exa_root" directory (see :mod:`~exa._config`).

    Args:
        persist (bool): Persistent install (default false)
        verbose (bool): Verbose installation (default false)
    '''
    if perisit == True:
        raise NotImplementedError()
    else:
        temporary()


def install_static(drop=False, verbose=False):
    '''
    Installs static data: database conversion tables and Jupyter notebook extensions

    Args:
        drop (bool): Drop static data before loading (required for persistent install)
        verbose (bool): Verbose notebook extension installation
    '''
    if drop == True:
        try:
            drop_all_static_tables()
        except:
            pass
    init_db()
    create_tables()
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
    install_notebook_widgets(config['nbext_localdir'], config['nbext_sysdir'], verbose)


def load_isotope_data():
    '''
    Load isotope data (from isotopes.json) into the database.
    '''
    df = pd.read_json(mkp(config['static'], 'isotopes.json'), orient='values')
    df.columns = ('A', 'Z', 'af', 'eaf', 'color', 'radius', 'gfactor', 'mass', 'emass',
                  'name', 'eneg', 'quadmom', 'spin', 'symbol', 'szuid', 'strid')
    df.index.names = ['pkid']
    df.reset_index(inplace=True)
    df.to_sql(name='isotope', con=engine, index=False, if_exists='replace')


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
        df_to_save.to_sql(name=column, con=engine, index=False, if_exists='replace')


def load_constant_data():
    '''
    Load constants (from constants.json) into the database.
    '''
    df = pd.read_json(mkp(config['static'], 'constants.json'))
    df.reset_index(inplace=True)
    df.columns = ['symbol', 'value']
    df['pkid'] = df.index
    df.to_sql(name='constant', con=engine, index=False, if_exists='replace')


def install_notebook_widgets(origin_base, dest_base, verbose=False):
    '''
    Convenience wrapper around :py:func:`~notebook.install_nbextension` that
    organizes notebook extensions for exa and related packages in a systematic
    fashion.
    '''
    try:
        shutil.rmtree(dest_base)
    except:
        pass
    for root, subdirs, files in os.walk(origin_base):
        for filename in files:
            subdir = root.split('nbextensions')[-1]
            orig = mkp(root, filename)
            dest = mkp(dest_base, subdir, mk=True)
            install_nbextension(orig, verbose=verbose, overwrite=True, nbextensions_dir=dest)


def drop_all_static_tables():
    '''
    Deletes all static (unit, isotope, and constant) tables.
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
    Isotope.__table__.drop(engine)
    Constant.__table__.drop(engine)
