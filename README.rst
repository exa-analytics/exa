| |logo|
##################
Installation
##################
| |conda|
| |pypi|
Exa is available through `anaconda`_,

.. code-block:: bash

    conda install -c exaanalytics exa

or `pypi`_.

.. code-block:: bash

    pip install exa

After installation, run the following to set up visualization.

.. code-block:: bash

    exa -u

###################
Getting Started
###################
| |docs|
| |gitter|
Documentation can be built using `sphinx`_:

.. code-block:: bash

    cd doc
    make html    # or .\make.bat html

##################
Status
##################
| |build|
| |issues|
| |cov|

###############
Legal
###############
| |lic|
| Copyright (c) 2015-2016, Exa Analytics Development Team
| Distributed under the terms of the Apache License 2.0

.. _anaconda: https://www.continuum.io/downloads
.. _pypi: https://pypi.python.org/pypi
.. _sphinx: http://www.sphinx-doc.org/en/stable/


.. |logo| image:: doc/source/_static/logo.png
    :target: doc/source/_static/logo.png
    :alt: Exa Analytics

.. |build| image:: https://travis-ci.org/exa-analytics/exa.svg?branch=master
    :target: https://travis-ci.org/exa-analytics/exa
    :alt: Build Status

.. |docs| image:: https://readthedocs.org/projects/exa/badge/?version=latest
    :target: http://exa.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |conda| image:: https://anaconda.org/exaanalytics/exa/badges/installer/conda.svg
    :target: https://conda.anaconda.org/exaanalytics
    :alt: Anaconda Version

.. |pypi| image:: https://badge.fury.io/py/exa.svg
    :target: https://badge.fury.io/py/exa
    :alt: PyPI Version

.. |gitter| image:: https://badges.gitter.im/exa-analytics/exa.svg
   :alt: Join the chat at https://gitter.im/exa-analytics/exa
   :target: https://gitter.im/exa-analytics/exa?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |issues| image:: https://www.quantifiedcode.com/api/v1/project/3c8a5fe969f745f8b2f3554ad59590f0/badge.svg
    :target: https://www.quantifiedcode.com/app/project/3c8a5fe969f745f8b2f3554ad59590f0
    :alt: Code Issues

.. |cov| image:: https://coveralls.io/repos/github/exa-analytics/exa/badge.svg
    :target: https://coveralls.io/github/exa-analytics/exa
    :alt: Code Coverage

.. |lic| image:: http://img.shields.io/:license-apache-blue.svg?style=flat-square
    :target: http://www.apache.org/licenses/LICENSE-2.0
    :alt: License
