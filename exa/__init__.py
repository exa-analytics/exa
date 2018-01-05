# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This package provides the :class:`~exa.core.container.Container` object
for data processing, analysis, and storage. The Container faciltates
easy manipulation and saving to `HDF` for scalars, lists, tuples, and `numpy`
and `pandas` objects via a single method.

.. code-block:: python

    c = Container(a=array, b=scalar, c=dataframe)
    c.to_hdf("my.hdf")                  # Saves a, b, and c to the HDF file "my.hdf"

    # "my.hdf" can be ready by any program/programming language that has support
    # for he HDF format. Using exa it can be down this way.
    d = Container.from_hdf("my.hdf")    # Reads in and attaches a, b, and c

This package also provides functionality for manipulation of text files on
permanent storage using a text-editor-like object, :class:`~exa.core.editor.Editor`.

.. code-block:: python

    ed = Editor("myfile.txt")
    ed.find("text")      # Finds all lines with "text"
    # Uses regular expressions to find lines ending with a digit followed by space
    ed.regex("\d\s$")
    ed_mod = ed.replace("a", b")    # Replace all occurances of "a" with "b"
    ed_mod.write("newfile.txt")     # Write file to permanent storage

The :class:`~exa.core.editor.Editor` objects are extended to provide text file
:class:`~exa.core.parser.Parser`s and :class:`~exa.core.composer.Composer`s
which facilitate conversion of complex text formats to systematic data structures
(as :class:`~exa.core.container.Container`s) and vice versa.

Although :class:`~exa.core.container.Container`s can accept any kind of named
data, they are most effective when constructed expecting certain named data
structures from which processing and analysis can be facilitated (since data of
known form is contained as a known attribute).

Finally, using the `Jupyter` notebook ecosystem and Python data stack, exa can
be used to build data computation, processing, analysis, and visualization
programs tailored to specific tasks, industires, or scientific niches.

See Also:
    This package provides a base class for constructing class objects with
    strongly typed attributes. See :mod:`~exa.typed` for more information.

.. _numpy: http://www.numpy.org/
.. _pandas: https://pandas.pydata.org/
.. _HDF: https://en.wikipedia.org/wiki/Hierarchical_Data_Format_
.. _Jupyter: https://jupyter.org/
"""
def _jupyter_nbextension_paths():
    """Jupyter notebook extension directory paths."""
    return [{
        'section': "notebook",
        'src': "static/nbextension",
        'dest': "exa",
        'require': "exa/extension"
    }]


from ._version import __version__
from .typed import Typed, TypedClass, TypedMeta, typed
from .core import (DataFrame, DataSeries, SparseDataSeries, SparseDataFrame,
                   Editor, Parser, Composer, Container, Column, Index, Field)
