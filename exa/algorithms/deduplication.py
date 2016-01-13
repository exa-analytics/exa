# -*- coding: utf-8 -*-
'''
Deduplication of Elements in a Collection
============================================
'''


def deduplicate_with_prev_offset(values, prev_offset=1):
    '''
    '''
    prev = values[0]
    dedup = []
    for value in values:
        if prev + prev_offset != value:
            dedup.append(value)
        prev = value
    return dedup
