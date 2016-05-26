# -*- coding: utf-8 -*-
'''
Configuration
====================================
This module determines what type of Python session is being used (Jupyter
notebook or other) and what optional dependencies are installed.
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


def show_conf():
    '''
    Read-only representation of the current configuration.

    .. code-block:: Python

        >>> 'exa_root' in _conf
        True
    '''
    pprint.pprint(_conf)


def _cleanup():
    '''
    Remove root directory in non-persistent session.
    '''
    if not _conf['exa_persistent']:
        shutil.rmtree(_conf['exa_root'])


_conf = {}    # Global configuration object
# System specific _confuration (exa_persistent _conf independent)
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
_conf['log_db'] = mkp(_conf['exa_root'], 'db.log')
_conf['log_sys'] = mkp(_conf['exa_root'], 'sys.log')
_conf['log_user'] = mkp(_conf['exa_root'], 'user.log')
_conf['logfile_max_bytes'] = 1048576
_conf['logfile_max_count'] = 5


# Internal package paths
pkg = os.path.dirname(__file__)
_conf['web_templates'] = mkp(pkg, '_web', 'templates')
_conf['web_html'] = mkp(pkg, '_web', 'html')
_conf['web_css'] = mkp(pkg, '_web', 'css')
_conf['web_js'] = mkp(pkg, '_web', 'js')
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
_conf['pkg_ipyparallel'] = False
_conf['pkg_cython'] = False
_conf['pkg_dask'] = False
_conf['pkg_distributed'] = False
try:
    import numba
    _conf['pkg_numba'] = True
except:
    pass
try:
    import ipyparallel
    _conf['pkg_ipyparallel'] = True
except:
    pass
try:
    import cython
    _conf['pkg_cython'] = True
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
    with open(existing_conf) as f:
        _conf.update(json.load(f))
