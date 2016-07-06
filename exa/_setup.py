# -*- coding: utf-8 -*-
'''
Setup
########################
This module generates the "~/.exa" directory where all databases, logs, notebooks,
and data reside and creates the configuration object (config).
'''
import os
import sys
import atexit
import platform
import configparser
import warnings
from exa.utility import mkp


def save():
    '''
    Save the configuration file to disk.
    '''
    with open(config_file, 'w') as f:
        config.write(f)


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
# log
if config['log']['syslog'] == 'None':
    config['log']['syslog'] = mkp(root, 'sys.log')
if config['log']['dblog'] == 'None':
    config['log']['dblog'] = mkp(root, 'db.log')


atexit.register(save)                             # Register
