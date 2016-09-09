# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Configuration
########################
This module generates the "~/.exa" directory where all databases, logs, notebooks,
and data reside by default.

[paths]
data: Path to the data directory (default ~/.exa/data)
notebooks: Path to the notebooks directory (default ~/.exa/notebooks)

[logging]
nlogs: Number of log files to rotate
nbytes: Max log file size (in bytes)
syslog: System log file path
dblog: Database log file path (if necessary)
level: Logging level, 0: normal, 1: extra info, 2: debug

[db]
uri: String URI for database connection
"""
import os
import sys
import atexit
import platform
import configparser
import shutil
import pandas as pd
from sqlalchemy import create_engine
from itertools import product


@atexit.register
def save():
    """
    Save the configuration file to disk (occurs automatically on exit).

    Warning:
        To ensure that changes to the configuration persist, only alter the
        configuration from one instance of exa, or by hand when exa has not
        been imported.
    """
    del config['dynamic']    # Delete dynamically assigned configuration options
    with open(config_file, "w") as f:
        config.write(f)


def mkdir(path):
    """
    Safely create a directory.
    """
    try:    # This approach supports Python 2 and Python 3
        os.makedirs(path)
    except OSError:
        pass


def init():
    """
    Copy tutorial.ipynb to the notebooks directory and update static db data.
    """
    tut = "tutorial.ipynb"
    tutorial_source = os.path.join(config['dynamic']['examples'], tut)
    tutorial_dest = os.path.join(config['paths']['notebooks'], tut)
    shutil.copy(tutorial_source, tutorial_dest)
    # Load isotope static data (replacing existing data)
    isotopes = os.path.join(config['dynamic']['data'], 'isotopes.json')
    df = pd.read_json(isotopes, orient='values')
    df.columns = ('A', 'Z', 'af', 'eaf', 'color', 'radius', 'gfactor', 'mass',
                  'emass', 'name', 'eneg', 'quadmom', 'spin', 'symbol', 'szuid',
                  'strid')
    df.index.names = ['pkid']
    df.reset_index(inplace=True)
    df.to_sql(name='isotope', con=engine, index=False, if_exists='replace')
    # Compute and load unit conversions
    path = os.path.join(config['dynamic']['data'], 'units.json')
    df = pd.read_json(path)
    for column in df.columns:
        series = df[column].dropna()
        values = series.values
        labels = series.index
        n = len(values)
        factor = (values.reshape(1, n) / values.reshape(n, 1)).ravel()
        from_unit, to_unit = zip(*product(labels, labels))
        df_to_save = pd.DataFrame.from_dict({'from_unit': from_unit,
                                             'to_unit': to_unit,
                                             'factor': factor})
        df_to_save['pkid'] = df_to_save.index
        df_to_save.to_sql(name=column, con=engine, index=False, if_exists='replace')


# The following sets up the configuration variable and database engine
config = configparser.ConfigParser()
# Get exa"s root directory (e.g. /home/[username]/.exa, C:\\Users\[username]\\.exa)
home = os.getenv("USERPROFILE") if platform.system().lower() == "windows" else os.getenv("HOME")
root = os.path.join(home, ".exa")
mkdir(root)
# Check for existing config or build one anew
config_file = os.path.join(root, "config")
init_flag = False
if os.path.exists(config_file):
    stats = os.stat(config_file)
    if stats.st_size > 180:      # Check that the file size > 180 bytes
        config.read(config_file)
else:
    # paths
    config['paths'] = {}
    config['paths']['data'] = os.path.join(root, "data")
    config['paths']['notebooks'] = os.path.join(root, "notebooks")
    mkdir(config['paths']['data'])
    mkdir(config['paths']['notebooks'])
    # logging
    config['logging'] = {}
    config['logging']['nlogs'] = "3"
    config['logging']['nbytes'] = str(10*1024*1024)    # 10 MiB
    config['logging']['syslog'] = os.path.join(root, "sys.log")
    config['logging']['dblog'] = os.path.join(root, "db.log")
    config['logging']['level'] = "0"
    # db
    config['db'] = {}
    config['db']['uri'] = "sqlite:///" + os.path.join(root, "exa.sqplite")
    init_flag = True

# Get the dynamic (system/installation/dev dependent) configuration
config['dynamic'] = {}
config['dynamic']['pkg'] = os.path.dirname(os.path.realpath(__file__))
config['dynamic']['root'] = root
config['dynamic']['data'] = os.path.join(config['dynamic']['pkg'], "..", "data")
config['dynamic']['examples'] = os.path.join(config['dynamic']['pkg'], "..", "examples")
config['dynamic']['numba'] = "false"
config['dynamic']['cuda'] = "false"
config['dynamic']['notebook'] = "false"
try:
    import numba
    config['dynamic']['numba'] = "true"
except ImportError:
    pass
try:
    from numba import cuda
    if len(cuda.devices.gpus) > 0:
        config['dynamic']['cuda'] = "true"
except (AttributeError, ImportError):
    pass
try:
    cfg = get_ipython().config
    if "IPKernelApp" in cfg:
        config['dynamic']['notebook'] = "true"
except NameError:
    pass

# Database engine
engine = create_engine(config['db']['uri'])

if init_flag:
    # Initialize static data
    init()
