# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Pair Summations
####################
Combinatorial or permutational pairwise summations often on non-numeric data.
"""
from itertools import product
from exa.workflow.dispatch import dispatch


@dispatch(list, list)
def product_pair_sum(x, y):
    """
    """
    return [xx + yy for xx, yy in product(x, y)]
