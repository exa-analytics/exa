# -*- coding: utf-8 -*-
'''
Parsing Support
================================

'''
import linecache
from exa import re, pd


def read_tsv(path, names, header=None, skip_blank_lines=False, **kwargs):
    '''
    Wrapper around :func:`~pandas.read_csv` for space delimited files with
    some convenient defaults.
    '''
    return pd.read_csv(path, delim_whitespace=True, header=header,
                       skip_blank_lines=skip_blank_lines, names=names, **kwargs)


def get_lines(path, lines):
    '''
    Extract specific lines (by line number - 1 based) from a file.

    Args
        path (str): String file path
        lines: List (or list like) of line numbers

    Returns
        data (list): List of extracted lines
    '''
    data = []
    for line in lines:
        data.append(linecache.getline(path, line))
    return data
