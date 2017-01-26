# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa uses the `Jupyter notebook`_ as a frontend for interactive data management,
computation, analytics, and visualization.

- :mod:`~exa.app.pyjs.__init__`: Custom notebook widgets infrastructure
- :mod:`~exa.app.nb`: Notebook application

See Also:
    For more information about how (ipy)widgets interact with the
    `Jupyter notebook`_, see the `ipywidgets`_ and `pythreejs`_. The launcher
    script is in :mod:`~exa.__main__`.

.. _Jupyter notebook: http://jupyter.org/
.. _ipywidgets: https://github.com/ipython/ipywidgets
.. _pythreejs: https://github.com/jovyan/pythreejs
"""
# Import base modules
from exa.app import nb

# Import sub-packages
from exa.app import tests, pyjs

# Import user/dev API
from exa.app.nb import Notebook
