.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0


########################
Installation
########################
For information on installing Python see https://www.python.org/ or
https://www.continuum.io/downloads (`Anaconda`_ is the recommended installation
method for Python; see also `Miniconda`_). Exa is **Python 2.7+** software.

Using `Anaconda`_ or `Miniconda`_

.. code-block:: bash

    conda install -c exaanalytics exa

Using `pip`_:

.. code-block:: bash

    pip install exa
    jupyter nbextension enable --py --sys-prefix exa

From tha `source`_:

.. code-block:: bash

    cd exa-source/    # contains setup.py
    python setup.py install
    jupyter nbextension enable --py --sys-prefix exa

For a development installation (npm required):

.. code-block:: bash

    git clone https://github.com/exa-analytics/exa.git
    cd exa
    pip install -e .
    jupyter nbextension install --py --symlink --sys-prefix exa
    jupyter nbextension enable --py --sys-prefix exa

.. note::
    
    Development on Windows may not be fully supported. Some convience scripts
    are provided in the ``docs`` and ``js`` directories.


.. _Anaconda: https://www.continuum.io/downloads
.. _Miniconda: http://conda.pydata.org/miniconda.html
.. _pip: https://docs.python.org/3.5/installing/
.. _source: https://github.com/exa-analytics/exa/releases
