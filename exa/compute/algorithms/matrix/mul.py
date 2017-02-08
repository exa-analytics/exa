# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Matrix Multiplication
##########################################
"""
import numpy as np
from exa.workflow.dispatch import dispatch


@dispatch(np.ndarray, np.ndarray)
def mul(a, b):
    """
    Matrix multiplication using numpy.
    """
    return np.matrix(a)*np.matrix(b)
