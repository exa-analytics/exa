.. Copyright (c) 2015-2016, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0


###################################################
Configuration and Logging
###################################################
Exa requires the creation of a persistent directory, **~/.exa** (e.g.
C:\\Users\\[username]\\.exa, /home/[username]/.exa) that houses the
configuration, logs, and content management system (CMS, which includes data
and analytics `notebooks`_). Although many of Exa's features do not require
a graphical interface, visualization does and is accomplished via `notebooks`_.

.. automodule:: exa._config
    :members:

.. automodule:: exa._version
    :members:

.. _notebooks: http://jupyter.org/
