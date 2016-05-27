# -*- coding: utf-8 -*-
'''
Configuration
##################################
This package can be imported in a dynamic (usual) way:

.. code-block:: Python

    import exa

All features of the package and dependencies will be available except
the automatic content management. This module keeps track of working
configuration options for persistent functionality such as content
management.

The configuration object is a simple dictionary **config** with the following
attributes (string keys in the config dictionary).

Attributes:
    app_css (str): Location of the app's css directory
    app_html (str): Location of the app's html directory
    app_js (str): Location of the app's js directory
    app_templates (str): Location of the app's (html) templates directory
    exa_persistent (bool): True is persistent session (exa._install.install was run perviously)
    exa_relational (str): Path to relational database
    exa_root (str): Root directory for exa session
    log_db (str): db.log filepath
    log_sys (str): sys.log filepath
    log_user (str): user.log filepath
    logfile_max_bytes (int): Rotating logfile max size (default 10MiB)
    logfile_max_count (int): Max number of rotating logs (default 5)
    nbext_localdir (str): Package directory where (Jupyter) notebook extensions are contained
    nbext_sysdir (str): System wide notebook extensions should be installed
    notebook (bool): True if running a Jupyter notebook session or not
    pkg_dask (bool): True if `dask`_ is installed
    pkg_distributed (bool): True if `distributed`_ is installed
    pkg_numba (bool): True if `numba`_ is installed
    static_constants.json (str): Location of the constants.json file
    static_isotopes.json (str): Location of the isotopes.json file
    static_units.json (str): Location of the units.json file

See Also:
    :mod:`~exa._install`
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


def save_config():
    with open(mkp(config['exa_root'], _filename), 'w') as f:
        json.dump(config, f)


def update_config():
    '''
    Populates the exa's configuration dictionary, **config**.
    '''
    global config
    dot_exa = None
    config['exa_persistent'] = False
    if platform.system().lower() == 'windows':
        dot_exa = mkp(os.getenv('USERPROFILE'), '.exa')
    else:
        dot_exa = mkp(os.getenv('HOME'), '.exa')
    if os.path.exists(dot_exa):
        config['exa_root'] = dot_exa
        config['exa_persistent'] = True
    else:
        config['exa_root'] = mkdtemp()
    config['debug'] = False
    config['log_db'] = mkp(config['exa_root'], 'db.log')
    config['log_sys'] = mkp(config['exa_root'], 'sys.log')
    config['log_user'] = mkp(config['exa_root'], 'user.log')
    config['logfile_max_bytes'] = 1048576
    config['logfile_max_count'] = 5


    # Internal package paths
    pkg = os.path.dirname(__file__)
    config['app_templates'] = mkp(pkg, '_app', 'templates')
    config['app_html'] = mkp(pkg, '_app', 'html')
    config['app_css'] = mkp(pkg, '_app', 'css')
    config['app_js'] = mkp(pkg, '_app', 'js')
    config['static_constants.json'] = mkp(pkg, '_static', 'constants.json')
    config['static_isotopes.json'] = mkp(pkg, '_static', 'isotopes.json')
    config['static_units.json'] = mkp(pkg, '_static', 'units.json')
    config['nbext_localdir'] = mkp(pkg, '_nbextensions')
    config['nbext_sysdir'] = mkp(jupyter_data_dir(), '_nbextensions', 'exa')


    # Check what type of Python session this is (python/ipython or jupyter notebook)
    config['notebook'] = False
    try:
        cfg = get_ipython().config
        if 'IPKernelApp' in cfg:
            config['notebook'] = True
    except:
        pass


    # Check what optional packages are available
    config['pkg_numba'] = False
    config['pkg_dask'] = False
    config['pkg_distributed'] = False
    try:
        import numba
        config['pkg_numba'] = True
    except:
        pass
    try:
        import dask
        config['pkg_dask'] = True
    except:
        pass
    try:
        import distributed
        config['pkg_distributed'] = True
    except:
        pass


    # Set default relational database
    config['exa_relational'] = 'sqlite:///{}'.format(mkp(config['exa_root'], 'exa.sqlite'))


    # Update the configuration if existing configuration exists
    existingconfig = mkp(config['exa_root'], _filename)
    if config['exa_persistent'] and os.path.exists(existingconfig):
        config = {}
        with open(existingconfig) as f:
            config = json.load(f)
        # Not all configurations can simply be updated: handle them manually
        config['debug'] = config['debug']


def cleanup():
    '''
    Remove root directory in non-persistent session.
    '''
    if config['exa_persistent']:
        save_config()
    else:
        shutil.rmtree(config['exa_root'])

update_config()
