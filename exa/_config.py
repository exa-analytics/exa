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

The configuration object is a simple dictionary **_conf** with the following
attributes (string keys in the _conf dictionary).

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
_conf = {}    # Global configuration object


def save_config():
    with open(mkp(_conf['exa_root'], _filename), 'w') as f:
        json.dump(_conf, f)


def update_config():
    '''
    Populates the exa's configuration dictionary, **_conf**.
    '''
    dot_exa = None
    _conf['exa_persistent'] = False
    if platform.system().lower() == 'windows':
        dot_exa = mkp(os.getenv('USERPROFILE'), '.exa')
    else:
        dot_exa = mkp(os.getenv('HOME'), '.exa')
    if os.path.exists(dot_exa):
        _conf['exa_root'] = dot_exa
        _conf['exa_persistent'] = True
    else:
        _conf['exa_root'] = mkdtemp()
    _conf['debug'] = False
    _conf['log_db'] = mkp(_conf['exa_root'], 'db.log')
    _conf['log_sys'] = mkp(_conf['exa_root'], 'sys.log')
    _conf['log_user'] = mkp(_conf['exa_root'], 'user.log')
    _conf['logfile_max_bytes'] = 1048576
    _conf['logfile_max_count'] = 5


    # Internal package paths
    pkg = os.path.dirname(__file__)
    _conf['app_templates'] = mkp(pkg, '_app', 'templates')
    _conf['app_html'] = mkp(pkg, '_app', 'html')
    _conf['app_css'] = mkp(pkg, '_app', 'css')
    _conf['app_js'] = mkp(pkg, '_app', 'js')
    _conf['static_constants.json'] = mkp(pkg, '_static', 'constants.json')
    _conf['static_isotopes.json'] = mkp(pkg, '_static', 'isotopes.json')
    _conf['static_units.json'] = mkp(pkg, '_static', 'units.json')
    _conf['nbext_localdir'] = mkp(pkg, '_nbextensions')
    _conf['nbext_sysdir'] = mkp(jupyter_data_dir(), '_nbextensions', 'exa')


    # Check what type of Python session this is (python/ipython or jupyter notebook)
    _conf['notebook'] = False
    try:
        cfg = get_ipython().config
        if 'IPKernelApp' in cfg:
            _conf['notebook'] = True
    except:
        pass


    # Check what optional packages are available
    _conf['pkg_numba'] = False
    _conf['pkg_dask'] = False
    _conf['pkg_distributed'] = False
    try:
        import numba
        _conf['pkg_numba'] = True
    except:
        pass
    try:
        import dask
        _conf['pkg_dask'] = True
    except:
        pass
    try:
        import distributed
        _conf['pkg_distributed'] = True
    except:
        pass


    # Set default relational database
    _conf['exa_relational'] = 'sqlite:///{}'.format(mkp(_conf['exa_root'], 'exa.sqlite'))


    # Update the _confuration if existing _confuration exists
    existing_conf = mkp(_conf['exa_root'], _filename)
    if _conf['exa_persistent'] and os.path.exists(existing_conf):
        config = {}
        with open(existing_conf) as f:
            config = json.load(f)
        # Not all configurations can simply be updated: handle them manually
        _conf['debug'] = config['debug']


def _cleanup():
    '''
    Remove root directory in non-persistent session.
    '''
    if _conf['exa_persistent']:
        save_config()
    else:
        shutil.rmtree(_conf['exa_root'])


update_config()    # Populate the _conf variable
