# -*- coding: utf-8 -*-
'''
Installer
########################
This module allows a user to install exa in a persistent manner enabling some
advanced content management features. Installation will create a permanent
directory where exa's relational database will be housed (default ~/.exa).
All container creation, logging, and static data is housed in this directory.

See Also:
    :mod:`~exa._config`
'''
from exa._config import config, dot_path
from exa.relational import install_db
from exa.widget import install_notebook_widgets


def install(persist=False, verbose=False):
    '''
    Sets up the database and Jupyter notebook extensions. If install with
    persistence, will perform setup in the "exa_root" directory (see :mod:`~exa._config`).

    Args:
        persist (bool): Persistent install (default false)
        verbose (bool): Verbose installation (default false)
    '''
    global config    # Whenever you modify a "global" variable, need to explicitly state global
    if persist == True:
        print('here?')
        config['exa_root'] = dot_path(True)
    install_db()
    install_notebook_widgets(config['nbext_localdir'], config['nbext_sysdir'], verbose)
