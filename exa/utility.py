# -*- coding: utf-8 -*-
'''
Utility Functions
====================
These functions are simply syntactic sugar. They help cleanup the code base by
providing a cleaner API for commonly used functions.
'''
import os
import shutil
from uuid import uuid4
from datetime import datetime
from notebook import install_nbextension


sep2 = os.sep + os.sep


def datetime_header():
    '''
    Creates a simple header string containing the current date/time stamp
    delimited using "=".
    '''
    return '\n'.join(('=' * 80, str(datetime.now()), '=' * 80))


def uid(as_hex=True):
    '''
    Generate a unique id (uuid4).

    Args:
        as_hex (bool): If True return hex string

    Returns:
        uid: String unique id or UUID object
    '''
    if as_hex:
        return uuid4().hex
    else:
        return uuid4()


def mkp(*args, mk=False, exist_ok=True):
    '''
    Generate a directory path, and create it if requested.

    .. code-block:: Python

        filepath = mkpath('base', 'folder', 'file')
        mkpath('base', 'folder', mkdir=True)

    Args
        \*args: File or directory path segments to be concatenated
        mk (bool): Make the directory (returns None)
        exist_ok (bool): Don't raise warning if director already exists (default True)

    Returns
        path (str): OS aware file or directory path
    '''
    path = os.sep.join(list(args))
    if mk:
        while sep2 in path:
            path = path.replace(sep2, os.sep)
        os.makedirs(path, exist_ok=exist_ok)
    return path


def _install_notebook_widgets(origin_base, dest_base, verbose=False):
    '''
    Convenience wrapper around :py:func:`~notebook.install_nbextension` that
    installs Jupyter notebook extensions using a systematic naming convention (
    mimics the source directory and file name structure rather than installing
    as a flat file set).

    Args:
        origin_base (str): Location of extension source code
        dest_base (str): Destination location (system and/or user specific)
        verbose (bool): Verbose installation (default False)

    Note:
        This function follows symbolic links (symlinks) and creates a copy of
        the linked file in the destination location.

    See Also:
        The configuration module :mod:`~exa._config` describes the default
        arguments used by :func:`~exa._install.install` during installation.
    '''
    try:
        shutil.rmtree(dest_base)
    except:
        pass
    for root, subdirs, files in os.walk(origin_base):
        for filename in files:
            subdir = root.split('nbextensions')[-1]
            orig = mkp(root, filename)
            dest = mkp(dest_base, subdir, mk=True)
            install_nbextension(orig, verbose=verbose, overwrite=True, nbextensions_dir=dest)


def del_keys(kwargs, match='id'):
    '''
    Delete certain keys in a dictionary containing a given string.

    Args:
        kwargs (dict): Dictionary to prune
        match (str): Sting to match for each key

    Return:
        d (dict): Pruned dictionary
    '''
    keys = [key for key in kwargs.keys() if match in key]
    for key in keys:
        del kwargs[key]
    return kwargs
