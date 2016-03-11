# -*- coding: utf-8 -*-
'''
Installer
====================
This module is responsible for initializing the database (whether in memory or
on disk/elsewhere) and installing/updating the (Jupyter) notebook widgets.
'''
import os
import pandas as pd
from itertools import product
from notebook import install_nbextension
from exa import _conf
from exa.utility import mkp
from exa.relational.base import _create_all, engine


def install(persistent=False):
    '''
    Initializes exa's database and notebook widget features.

    By default, exa runs in memory. To take full advantage of exa's content
    management features this function should be run. It will create a storage
    location in **~/.exa** where all configuration, log, and data are housed.

    Args:
        persistent (bool): If True, will install exa to the ~/.exa directory
    '''
    _create_all()
    _load_isotope_data()
    _load_unit_data()
    _load_constant_data()
    _install_notebook_widgets()


def _load_isotope_data():
    '''
    Load static isotope data into the database.
    '''
    df = pd.read_json(_conf['static_isotopes.json'])
    df.sort_values(['Z', 'A'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.reset_index(inplace=True)
    df['pkid'] = df['index']
    del df['index']
    df.to_sql(name='isotope', con=engine, index=False, if_exists='replace')


def _load_unit_data():
    '''
    Load static unit conversions into the database.
    '''
    df = pd.read_json(_conf['static_units.json'])
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


def _load_constant_data():
    '''
    Load static constants into the database.
    '''
    df = pd.read_json(_conf['static_constants.json'])
    df.reset_index(inplace=True)
    df.columns = ['symbol', 'value']
    df['pkid'] = df.index
    df.to_sql(name='constant', con=engine, index=False, if_exists='replace')


def _install_notebook_widgets(origin_base=_conf['nbext_localdir'],
                              dest_base=_conf['nbext_sysdir'], verbose=False):
    '''
    Installs custom :py:mod:`ipywidgets` JavaScript into the Jupyter
    nbextensions directory to allow use of exa's JavaScript frontend
    within the Jupyter notebook GUI.
    '''
    for root, subdirs, files in os.walk(origin_base):
        for filename in files:
            subdir = root.split('nbextensions')[-1]
            orig = mkp(root, filename)
            dest = mkp(dest_base, subdir, mk=True)
            install_nbextension(orig, verbose=verbose, overwrite=True, nbextensions_dir=dest)
