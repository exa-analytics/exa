[![exa logo](docs/source/_static/logo.png)](https://exa-analytics.github.io) 
*A framework for file parsing, data processing, and visualization*

# Installation
[![conda Badge](https://anaconda.org/avmarchenko/exa/badges/installer/conda.svg)](https://conda.anaconda.org/avmarchenko)  
[![pypi badge](https://badge.fury.io/py/exa.svg)](https://badge.fury.io/py/exa)  
Exa is available through [anaconda](https://www.continuum.io/downloads)

    $ conda install -c exaanalytics exa

or [pypi](https://pypi.python.org/pypi).

    $ pip install exa
    $ jupyter nbextension install exa --py --sys-prefix --overwrite
    $ jupyter nbextension enable exa --py --sys-prefix


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
[![travis](https://travis-ci.org/avmarchenko/exa.svg?branch=master)](https://travis-ci.org/exa-analytics/exa)  
[![Coverage](https://coveralls.io/repos/github/avmarchenko/exa/badge.svg?branch=master)](https://coveralls.io/github/avmarchenko/exa?branch=master)  
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/221e700665c74c85b8255e5b399490d4)](https://www.codacy.com/app/alexvmarch/exa?utm_source=github.com&utm_medium=referral&utm_content=avmarchenko/exa&utm_campaign=Badge_Coverage)

For a development ready installation:

    $ git clone https://github.com/avmarchenko/exa.git
    $ cd exa
    $ pip install -e .
    $ ./js/nmpinstall.sh    # or .\js\npminstall.bat

Note that this requires npm (Node.js).


# Reference
[![DOI](https://zenodo.org/badge/23807/exa-analytics/exa.svg)](https://zenodo.org/badge/latestdoi/23807/exa-analytics/exa)  


# Legal
[![Apache License 2.0](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0)  
Copyright (c) 2015-2017, Exa Analytics Development Team  
Distributed under the terms of the Apache License 2.0  
