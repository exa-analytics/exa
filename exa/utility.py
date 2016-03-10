# -*- coding: utf-8 -*-
'''
Utility Functions
====================
These functions are simply syntactic sugar. They help cleanup the code base by
providing a cleaner API for commonly used functions.
'''
__all__ = ['uid', 'mkp']


from os import makedirs as _mkdirs
from os import sep as _sep
from uuid import uuid4 as _uuid4


_sep2 = _sep + _sep


def uid(as_hex=True):
    '''
    Generate a unique id (uuid4).

    Args:
        as_hex (bool): If True return hex string

    Returns:
        uid: String unique id or UUID object
    '''
    if as_hex:
        return _uuid4().hex
    else:
        return _uuid4()


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
    path = _sep.join(list(args))
    if mk:
        while _sep2 in path:
            path = path.replace(_sep2, _sep)
        _mkdirs(path, exist_ok=exist_ok)
    return path
