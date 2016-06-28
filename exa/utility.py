# -*- coding: utf-8 -*-
'''
Utilities
#####################
These functions are simply syntactic sugar. They help cleanup the code base by
providing a cleaner API for commonly used functions.
'''
import os
import numpy as np
from datetime import datetime


sep2 = os.sep + os.sep
sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB']


def datetime_header(title=''):
    '''
    Creates a simple header string containing the current date/time stamp
    delimited using "=".
    '''
    return '\n'.join(('=' * 80, title + ': ' + str(datetime.now()), '=' * 80))


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


def convert_bytes(value):
    '''
    Reduces bytes to more convenient units (i.e. KiB, GiB, TiB, etc.).

    Args:
        values (int): Value in Bytes

    Returns:
        tup (tuple): Tuple of value, unit (e.g. (10, 'MiB'))
    '''
    n = np.rint(len(str(value))/4).astype(int)
    return value/(1024**n), sizes[n]
