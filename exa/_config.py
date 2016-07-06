# -*- coding: utf-8 -*-
'''
Configuration
##################################

'''
import os
import platform
import getpass
import json
import pprint
import shutil
import stat
from tempfile import mkdtemp
from notebook.nbextensions import jupyter_data_dir
from exa.utility import mkp


_filename = 'config.json'
config = {}


def dot_path(mk=False):
    '''
    Generate (and create if desired) the expected persistent exa path.
    '''
    if platform.system().lower() == 'windows':
        dot_exa = mkp(os.getenv('USERPROFILE'), '.exa', mk=mk)
    else:
        dot_exa = mkp(os.getenv('HOME'), '.exa', mk=mk)
    return dot_exa


def save_config():
    '''
    Dump the (text) configuration to a file.
    '''
    with open(mkp(config['exa_root'], _filename), 'w') as f:
        json.dump(config, f)


def update_config():
    '''
    Update (or initialize) the global configuration dictionary.
    '''
    global config
    dot_exa = None
    config['exa_persistent'] = False
    dot_exa = dot_path()
    if os.path.exists(dot_exa):
        config['exa_root'] = dot_exa
        config['exa_persistent'] = True
    else:
        config['exa_root'] = mkdtemp()
    config['runlevel'] = 0                      # Specifies verbosity for tests/logging
    config['log_db'] = mkp(config['exa_root'], 'db.log')
    config['log_sys'] = mkp(config['exa_root'], 'sys.log')
    config['log_user'] = mkp(config['exa_root'], 'user.log')
    config['logfile_max_bytes'] = 10485760      # 10 MB
    config['logfile_max_count'] = 5
    pkg = os.path.dirname(__file__)
    config['static'] = mkp(pkg, '_static')
    config['nbext_localdir'] = mkp(pkg, '_nbextension')
    config['nbext_sysdir'] = mkp(jupyter_data_dir(), 'nbextensions', 'exa')  # System path
    config['notebook'] = False    # Check if running in Jupyter notebook
    try:
        cfg = get_ipython().config
        if 'IPKernelApp' in cfg:
            config['notebook'] = True
    except:
        pass
    config['exa_relational'] = 'sqlite:///{}'.format(mkp(config['exa_root'], 'exa.sqlite'))
    existing_config = mkp(config['exa_root'], _filename)
    if config['exa_persistent'] and os.path.exists(existing_config):
        with open(existing_config) as f:
            econf = json.load(f)
        config['runlevel'] = econf['runlevel']    # Only update a select set of parameters
        config['logfile_max_bytes'] = econf['logfile_max_bytes']
        config['logfile_max_count'] = econf['logfile_max_count']
        config['log_db'] = econf['log_db']
        config['log_sys'] = econf['log_sys']
        config['log_user'] = econf['log_user']
        config['static'] = econf['static']


def cleanup():
    '''
    Remove root directory in non-persistent session.
    '''
    if config['exa_persistent']:
        save_config()
    else:
        shutil.rmtree(config['exa_root'])
