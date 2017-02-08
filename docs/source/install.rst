.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0


########################
Installation
########################
For information on installing Python see https://www.python.org/ or
https://wiki.python.org/moin/BeginnersGuide/Download. Exa supports
**Python 2.7+**. Installation via the `anaconda` (or `miniconda`_) Python
distribution is recommended.

.. code-block:: bash

    conda install -c exaanalytics exa

Alternatively using `pip`_:

.. code-block:: bash

    pip install exa
    jupyter nbextension enable --py --sys-prefix exa

Alternatively download the exa `source`_:

.. code-block:: bash

    cd exa-source/    # contains setup.py
    python setup.py install
    jupyter nbextension enable --py --sys-prefix exa

Finally, for a development installation (npm required):

.. code-block:: bash

    git clone https://github.com/exa-analytics/exa.git
    cd exa
    pip install -e .
    jupyter nbextension install --py --symlink --sys-prefix exa
    jupyter nbextension enable --py --sys-prefix exa

Note that the development installation does not support Windows.


.. _anaconda: https://www.continuum.io/downloads
.. _miniconda: http://conda.pydata.org/miniconda.html
.. _pip: https://docs.python.org/3.5/installing/
.. _source: https://github.com/exa-analytics/exa
