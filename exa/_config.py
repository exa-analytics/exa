# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Configuration
########################
This module generates the "~/.exa" directory where all databases, logs, notebooks,
and data reside by default.

[DEFAULT]
data: Path to the data directory (default ~/.exa/data)
notebooks: Path to the notebooks directory (default ~/.exa/notebooks)

[LOGGING]
nlogs: Number of log files to rotate
nbytes: Max log file size (in bytes)
syslog: System log file path
dblog: Database log file path (if necessary)
level: Logging level, 0: normal, 1: extra info, 2: debug

[DB]
uri: String URI for database connection
"""
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
    """
    Save the configuration file to disk (occurs automatically on exit).

    Warning:
        To ensure that changes to the configuration persist, only alter the
        configuration from one instance of exa, or by hand when exa has not
        been imported.
    """
    del config['dynamic']    # Delete dynamically assigned configuration options
    with open(config_file, 'w') as f:
        config.write(f)


# The following sets up the configuration variable, config
config = configparser.ConfigParser()

# Get exa's root directory (e.g. /home/[username]/.exa, C:\\Users\[username]\\.exa)
home = os.getenv('USERPROFILE') if platform.system().lower() == 'windows' else os.getenv('HOME')
root = os.path.join(home, '.exa')
try:
    os.makedirs(root)      # We mkdir like this to ensure py2 compatibility
except FileExistsError:
    pass
os.makedirs(root, exist_ok=True)
config_file = mkp(root, 'config')                 # Config file path
pkg = os.path.dirname(__file__)                   # Package source path
config.read(mkp(pkg, "..", "data", "config"))        # Read in default config
if os.path.exists(config_file):
    stats = os.stat(config_file)
    if stats.st_size > 180:
        config.read(config_file)                  # Read in existing config
# paths
if config['paths']['data'] == 'None':
    config['paths']['data'] = mkp(root, 'data', mk=True)
if config['paths']['notebooks'] == 'None':
    config['paths']['notebooks'] = mkp(root, 'notebooks', mk=True)
    shutil.copyfile(mkp(pkg, "..", "examples", 'tutorial.ipynb'),
                    mkp(root, 'notebooks', 'tutorial.ipynb'))
mkp(config['paths']['data'], 'examples', mk=True)  # Ensure the example dir is made
if config['paths']['update'] == '1':
    shutil.copyfile(mkp(pkg, "..", "examples", 'tutorial.ipynb'),
                    mkp(root, 'notebooks', 'tutorial.ipynb'))
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
    except Exception:
        pass
config['dynamic']['notebook'] = 'false'
try:
    cfg = get_ipython().config
    if 'IPKernelApp' in cfg:
        config['dynamic']['notebook'] = 'true'
except NameError:
    pass
