# -*- coding: utf-8 -*-
'''
Deduplication of Elements in a Collection
============================================
'''


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