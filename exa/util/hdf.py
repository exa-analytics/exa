# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
HDF Utilities
################
This module stores some hard-coded values related to saving to and from
HDF files using the `pandas`_ machinery.

.. _pandas: https://pandas.pydata.org
"""
_spec_name = "__exa_specials__"
_types_name = "__types__"
_forbidden = ("CLASS", "TITLE", "VERSION", "pandas_type", "pandas_version",
              "encoding", "index_variety", "name", original_types)
_conv = {'ss': pd.SparseSeries, 's': pd.Series,
         'sd': pd.SparseDataFrame, 'd': pd.DataFrame}
