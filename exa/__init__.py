# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
The purpose of this package is to provide a framework for reading data from disk,
organizing this data into related, systematic, and efficient data structures, and
attaching these data structures to a container to allow visualization and other
interactive exploration within the `Jupyter notebook`_. The following is a compact
summary.

- `editors`: Classes that facilitate creation of data containers
- `dataframe`: Classes that facilitate data visualization via the container
- `containers`: Flexible device for processing, analyzing and visualizing data

Complete documentation is available on the web https://exa-analytics.github.io/exa/.
The following is a brief description of the source code structure, which may aid
in usage.

- :mod:`~exa.core.editor`: Generic editors
- :mod:`~exa.core.parsing`: Parsing editors
- :mod:`~exa.core.dataframe`: Structured data objects
- :mod:`~exa.core.container`: Generic container

- :mod:`~exa.mpl`: Matplotlib wrappers
- :mod:`~exa.tex`: Text manipulation utilities
- :mod:`~exa.constants`: Physical constants
- :mod:`~exa.units`: Physical units
- :mod:`~exa.isotopes`: Chemical isotopes

- :mod:`~exa.spcial`: Singleton metaclass
- :mod:`~exa.core.base`: Abstract base classes

Note:
    Tests are always located in the ``tests`` directory of each package or
    sub-package.

.. _Jupyter notebook: https://jupyter.org/
"""
def _datadir():
    """Name of the static data directory."""
    return ("exa", "_data")

from ._version import __version__
from .core import DataFrame, Editor, Sections, Parser, Container
