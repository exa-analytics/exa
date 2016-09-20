.. Copyright (c) 2015-2016, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0


###################################################
Configuration, Logging, and Database Connectivity
###################################################
Exa requires the creation of a persistent directory, **~/.exa** (e.g.
C:\\Users\\[username]\\.exa, /home/[username]/.exa) that houses the
configuration, logs, content management database, and, by default, all data
and analytics notebooks (`Jupyter notebooks`_).

To take full advantage of the analytics and visualization features of this
framework, exa and its related packages should be run inside of a Jupyter
notebook. When using the workflow and other processing features, exa and its
related packages can be run inside of a notebook or in the console directly.

.. automodule:: exa._config
    :members:

.. automodule:: exa._version
    :members:


.. _Jupyter notebooks: http://jupyter.org/
