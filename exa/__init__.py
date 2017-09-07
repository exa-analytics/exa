# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa provides a framework for building data specific containers. Containers are
storage objects which house a collection of data objects (scalars, lists,
arrays, dataframes, images, etc.) and provide a unified API for processing,
analysis, and visualization.

Containers can be constructed from well organized data (such as HDF or CSV data
on disk) or from irregular or semi-regular text files (for example output from
another software). In order to facilitate the latter, exa provides editors,
parsers, and composers, which are used to programmatically manipulate text
data on disk.

Containers plug-in to exa's workflow framework which can be used to construct
data processing pipelines that are interoperable with external computational
resources (such as a dedicated computing cluster) and other features such as
out-of-core processing (for task too large to fit in RAM).

Note:
    Exa takes advantage of Python's extensive suite of tools for data science,
    including the `Jupyter notebook`_, `ipywidgets`_ framework, and `JIT`_
    compilation provided by `numba`_.

.. _Jupyter notebook: https://jupyter.org
.. _ipywidgets: https://ipywidgets.readthedocs.io
.. _JIT: https://en.wikipedia.org/wiki/Just-in-time_compilation
.. _numba: https://numba.pydata.org
"""
def _jupyter_nbextension_paths():
    """
    Jupyter notebook extension directory paths.

    Note:
        The `static` directory contains package data as well as JavaScript
        extensions (for use in the Jupyter notebook).
    """
    return [{'section': "notebook",
             'src': "static",
             'dest': "jupyter-exa",
             'require': "jupyter-exa/extension"}]


from ._version import __version__
from .editor import Editor
from .container import Container
