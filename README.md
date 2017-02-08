[![exa logo](docs/source/_static/logo.png)](https://exa-analytics.github.io)  


# Installation
[![conda Badge](https://anaconda.org/exaanalytics/exa/badges/installer/conda.svg)](https://conda.anaconda.org/exaanalytics)  
[![pypi badge](https://badge.fury.io/py/exa.svg)](https://badge.fury.io/py/exa)  
Exa is available through [anaconda](https://www.continuum.io/downloads)

    $ conda install -c exaanalytics exa

or [pypi](https://pypi.python.org/pypi).

    $ pip install exa
    $ jupyter nbextension enable --py --sys-prefix exa


# Getting Started
[![docs](https://readthedocs.org/projects/exa/badge/?version=latest)](https://exa-analytics.github.io/exa/)  
[![gitter](https://badges.gitter.im/exa-analytics/exa.svg)](https://gitter.im/exa-analytics/exa)  
Building the docs requires [sphinx](http://www.sphinx-doc.org/en/stable).
On Linux or Mac OS:

    $ cd docs
    $ make html

On Windows:

    $ cd docs
    $ ./make.bat html


# Contributing
[![travis](https://travis-ci.org/exa-analytics/exa.svg?branch=master)](https://travis-ci.org/exa-analytics/exa)  
[![Coverage](https://coveralls.io/repos/github/exa-analytics/exa/badge.svg?branch=master)](https://coveralls.io/github/exa-analytics/exa?branch=master)  
[![Codacy](https://api.codacy.com/project/badge/Grade/221e700665c74c85b8255e5b399490d4)](https://www.codacy.com/app/alexvmarch/exa?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=exa-analytics/exa&amp;utm_campaign=Badge_Grade)  

For a development ready installation:

    $ git clone https://github.com/exa-analytics/exa.git
    $ cd exa
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix exa
    $ jupyter nbextension enable --py --sys-prefix exa

Note that this requires npm and is not fully supported on Windows.


# Reference
[![DOI](https://zenodo.org/badge/23807/exa-analytics/exa.svg)](https://zenodo.org/badge/latestdoi/23807/exa-analytics/exa)  


# Legal
[![Apache License 2.0](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0)  
Copyright (c) 2015-2017, Exa Analytics Development Team  
Distributed under the terms of the Apache License 2.0  
