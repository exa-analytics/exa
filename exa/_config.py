# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Configuration
########################
This module generates the "~/.exa" directory where all databases, logs, notebooks,
and data reside. This configuration may be altered by editing the items below:

paths:
    - data: Path to the data directory (default ~/.exa/data)
    - notebooks: Path to the notebooks directory (default ~/.exa/notebooks)

log:
    - nlogs: Number of log files to rotate
    - nbytes: Max log file size (in bytes)
    - syslog: System log file path
    - dblog: Database log file path (if necessary)
    - level: Logging level, 0: normal, 1: extra info, 2: debug

db:
    - uri: String URI for database connection
    - update: If 1, refresh static database data (e.g. unit conversions)

js:
    - update: If 1, update JavaScript notebook extensions

Warning:
    The configuration file (~/.exa/config) should only be altered when no exa
    notebooks are running (i.e. exa or any of its related packages are imported).
'''
import os
import sys
import atexit
import platform
import configparser
import warnings
import shutil
from exa.utility import mkp


@atexit.register
def save():
    '''
    Save the configuration file to disk on exit, resetting update flags.

    Warning:
        This is a bit unsafe because we are not guarenteed to hit the updating
        function during execution (that is what well written tests are for -
        use **mock**), but it is advantageous in the case that multiple packages
        that use exa are running simultaneously.
    '''
    del config['dynamic']    # Delete dynamically assigned configuration options
    with open(config_file, 'w') as f:
        config.write(f)


def set_update():
    '''
    Set update flags.
    '''
    config['paths']['update'] = '1'
    config['js']['update'] = '1'
    config['db']['update'] = '1'


def del_update():
    '''
    Reset update flags.
    '''
    config['paths']['update'] = '0'
    config['js']['update'] = '0'
    config['db']['update'] = '0'


config = configparser.ConfigParser()              # Application configuration
if platform.system().lower() == 'windows':        # Get exa's root directory
    home = os.getenv('USERPROFILE')
else:
    home = os.getenv('HOME')
root = mkp(home, '.exa', mk=True)                 # Make exa root directory
config_file = mkp(root, 'config')                 # Config file path
pkg = os.path.dirname(__file__)                   # Package source path
if os.path.exists(config_file):
    config.read(config_file)                      # Read in existing config
else:
    config.read(mkp(pkg, '_static', 'config'))    # Read in default config
# paths
if config['paths']['data'] == 'None':
    config['paths']['data'] = mkp(root, 'data', mk=True)
if config['paths']['notebooks'] == 'None':
    config['paths']['notebooks'] = mkp(root, 'notebooks', mk=True)
    shutil.copyfile(mkp(pkg, '_static', 'exa_demo.ipynb'),
                    mkp(root, 'notebooks', 'exa_demo.ipynb'))
if config['paths']['update'] == '1':
    shutil.copyfile(mkp(pkg, '_static', 'exa_demo.ipynb'),
                    mkp(root, 'notebooks', 'exa_demo.ipynb'))
    atexit.register(del_update)
#log
if config['log']['syslog'] == 'None':
    config['log']['syslog'] = mkp(root, 'sys.log')
if config['log']['dblog'] == 'None':
    config['log']['dblog'] = mkp(root, 'db.log')
# db
if config['db']['uri'] == 'None':
    config['db']['uri'] = 'sqlite:///' + mkp(root, 'exa.sqlite') # SQLite by default
# dynamically allocated configurations (these are deleted before saving)
config['dynamic'] = {}
config['dynamic']['pkgdir'] = pkg
config['dynamic']['exa_root'] = root
nb = 'false'
try:
    import numba
    nb = 'true'
except ImportError:
    pass
config['dynamic']['numba'] = nb
config['dynamic']['cuda'] = 'false'
if config['dynamic']['numba'] == 'true':
    try:
        from numba import cuda
        if len(cuda.devices.gpus) > 0:
            config['dynamic']['cuda'] = 'true'
    except:
        pass
config['dynamic']['notebook'] = 'false'
try:
    cfg = get_ipython().config
    if 'IPKernelApp' in cfg:
        config['dynamic']['notebook'] = 'true'
except NameError:
    pass
