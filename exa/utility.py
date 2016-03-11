# -*- coding: utf-8 -*-
'''
Utility Functions
====================
These functions are simply syntactic sugar. They help cleanup the code base by
providing a cleaner API for commonly used functions.
'''
from os import makedirs
from os import sep
from uuid import uuid4
from datetime import datetime


sep2 = sep + sep


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
    path = sep.join(list(args))
    if mk:
        while sep2 in path:
            path = path.replace(sep2, sep)
        makedirs(path, exist_ok=exist_ok)
    return path
