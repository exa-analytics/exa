# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This package creates a framework for data management, computation, analytics,
and visualization. It is built atop the Python data stack (for more info see
`PyData`_) utilizing the `Jupyter notebook`_ interface as a user interface. The
base modules provide utility functionality utilized by the core sub-packages,
:mod:`~exa.cms`, :mod:`~exa.core`, :mod:`~exa.compute`.

- :mod:`~exa.__main__`: Application launchers
- :mod:`~exa._config`: Configuration and logging
- :mod:`~exa.tester`: Unit and doc tests
- :mod:`~exa.errors`: Loggable errors and exceptions
- :mod:`~exa.js`: Interactive visualizations (3d)
- :mod:`~exa.mpl`: Interactive visualizations (2d)
- :mod:`~exa.tex`: LaTeX support
- :mod:`~exa.typed`: Strongly typed class attributes

.. _PyData: http://pydata.org/
.. _Jupyter notebook: http://jupyter.org/
"""
# Import base modules
from exa import _version, _config, tester, errors, typed, mpl, tex

# Import sub-packages
from exa import cms, compute, core, tests, pyjs

# Import user/dev API
from exa._version import __version__, version_info
from exa._config import print_config
from exa.mpl import color_palette
from exa.cms import scoped_session, session_factory, db, File, Job, Project
from exa.core import Editor, CSV


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-exa',
        'require': 'jupyter-exa/extension'
    }]
