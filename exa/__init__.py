# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa provides a framework for building data specific containers. Containers are
storage objects which house a collection of data objects (scalars, lists,
arrays, dataframes, images, etc.) and provide a unified API for processing,
analysis, and visualization. The generic container has methods for inspecting
the collection of data it holds and for saving/loading that data to common
formats such as HDF.

Containers can be constructed from well organized data (such as HDF or CSV data
on disk) or from irregular or semi-regular text files (for example output from
another software). In order to facilitate the latter, exa provides editors,
parsers, and composers, which are used to programmatically manipulate text
data on disk.

Note:
    Exa can take advantage of Python's extensive suite of tools for data science,
    including the `Jupyter notebook`_, `ipywidgets`_ framework, and `JIT`_
    compilation provided by `numba`_, among others.

.. _Jupyter notebook: https://jupyter.org
.. _ipywidgets: https://ipywidgets.readthedocs.io
.. _JIT: https://en.wikipedia.org/wiki/Just-in-time_compilation
.. _numba: https://numba.pydata.org
"""
from ._version import __version__
from .typed import Typed, TypedClass, TypedMeta, typed
from .core import (DataFrame, DataSeries, SparseDataSeries, SparseDataFrame,
                   Editor, Parser, Composer, Container)
