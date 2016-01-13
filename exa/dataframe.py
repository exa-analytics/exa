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
    __dimensions__ = []
    __attributes__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.index.names) != len(self.__dimensions__):
            pass
