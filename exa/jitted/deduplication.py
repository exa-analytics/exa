# -*- coding: utf-8 -*-
'''
Jitted Deduplication of Elements in a Collection
===================================================
'''
from exa.jitted import jit, int64


@jit(nopython=True, cache=True)
def array1d_with_offset(array, offset=1):
    '''
    '''
    previous = array[0]
    deduped = []
    for element in array:
        if previous + offset != element:
            deduped.append(element)
        previous = element
    return deduped
