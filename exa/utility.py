# -*- coding: utf-8 -*-
'''
Helper Functions
====================
'''
import os
from uuid import uuid4
from itertools import product
from notebook import install_nbextension
from exa.config import Config


DBLSEP = os.sep + os.sep


def gen_uid(as_hex=True):
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


def mkpath(*args, mkdir=False):
    '''
    Creates an OS aware file or directory path string. If directory,
    can create on disk (if mkdir is True, default False). Does not
    throw a warning if the directory already exists.

    .. code-block:: Python

        filepath = mkpath('base', 'folder', 'file')
        mkpath('base', 'folder', mkdir=True)

    Args
        \*args: File or directory path segments to be concatenated
        mkdir (bool): Make the directory (returns None)

    Returns
        path (str): OS aware file or directory path
    '''
    path = os.sep.join(list(args))
    if mkdir:
        while DBLSEP in path:
            path = path.replace(DBLSEP, os.sep)
        os.makedirs(path, exist_ok=True)
    return path
