# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Version Information
#####################
The version can be checked any of the following ways.

.. code-block:: Python

    >>> exa.__verion__
    >>> help(exa)
    >>> exa._version.version_info
"""
version_info = (0, 4, 0)
__version__ = '.'.join(map(str, version_info))
