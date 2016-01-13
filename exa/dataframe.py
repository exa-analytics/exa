# -*- coding: utf-8 -*-
'''
Custom DataFrame for exa Analytics
====================================
'''
from exa import _pd as pd


class DataFrame(pd.DataFrame):
    '''
    Should behave just like a :py:class:`~pandas.DataFrame`.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
