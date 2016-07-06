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
from exa.utility import mkp


def save():
    '''
    Save the configuration file to disk.
    '''
    with open(config_file, 'w') as f:
        config.write(f)


# Begin setup
config = configparser.ConfigParser()              # Application configuration
if platform.system().lower() == 'windows':        # Get exa's root directory
    home = os.getenv('USERPROFILE')
else:
    home = os.getenv('HOME')
root = mkp(home, '.exa', mk=True, exist_ok=True)  # Make the exa root dir (if needed)
pkg = os.path.dirname(__file__)                   # Package source path
config_file = mkp(root, 'config')                 # Config file path
if os.path.exists(config_file):
    config.read(config_file)                      # Read in existing config
else:
    config.read(mkp(pkg, '_static', 'config'))    # Read in default config
for path in config['paths'].items():              # Create required paths
    print(path)








#from exa._config import config, dot_path
#from exa.relational import install_db
#from exa.widget import install_notebook_widgets
#
#
#def install(persist=False, verbose=False):
#    '''
#    Sets up the database and Jupyter notebook extensions. If install with
#    persistence, will perform setup in the "exa_root" directory (see :mod:`~exa._config`).
#
#    Args:
#        persist (bool): Persistent install (default false)
#        verbose (bool): Verbose installation (default false)
#    '''
#    global config    # Whenever you modify a "global" variable, need to explicitly state global
#    if persist == True:
#        print('here?')
#        config['exa_root'] = dot_path(True)
#    install_db()
#    install_notebook_widgets(config['nbext_localdir'], config['nbext_sysdir'], verbose)
#
