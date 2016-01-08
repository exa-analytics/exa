Getting Started
================
The exa package provides an executable that can be used to access application
features.

.. code-block:: bash

    exa -h    # Prints usage and help

As with all Python packages, exa can simply be imported inside any interpreter.

.. code-block:: Python

    >>> import exa
    >>> from exa import Length as L
    >>> exa.Project(name='Test Project')
    Project(None: 'Test Project')
    >>> L['km', 'm']
    1000
