# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa provides containers. Containers are Python classes which store or hold all
types of data, from numpy arrays to pandas dataframes to scikit images.
TODO: one sentence container value-add.

Containers can be constructed from well organized data (such as HDF or CSV data
on disk) or from irregular or semi-regular text files (for example output from
another software). In order to facilitate the latter, exa provides editors.
Editors, including parsers and composers can be utilized to programmatically
manipulated, parse, and compose text files into/out of container objects.

Specific data containers can also be used for data visualization. Exa provides
a widgets mechanism, built upon the `ipywidgets`_ framework for web-based data
exploration and complex visualizations within the `Jupyter notebook`_.

.. _ipywidgets: https://ipywidgets.readthedocs.io/
.. _Jupyter notebook: https://jupyter.org/
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


import seaborn    # Prevents nosetest error (Python 3.5, 3.6; Linux only)
from ._version import __version__
from .editor import Editor
