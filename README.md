[![exa logo](docs/source/_static/logo.png)](https://exa-analytics.github.io) 
*A framework for data processing, computation, and visualization*

# Installation
[![conda Badge](https://anaconda.org/avmarchenko/exa/badges/installer/conda.svg)](https://conda.anaconda.org/avmarchenko)  
[![pypi badge](https://badge.fury.io/py/exa.svg)](https://badge.fury.io/py/exa)  
Exa is available through [anaconda](https://www.continuum.io/downloads)

    $ conda install -c avmarchenko exa

or [pypi](https://pypi.python.org/pypi).

    $ pip install exa
    $ jupyter nbextension install exa --py --sys-prefix --overwrite
    $ jupyter nbextension enable exa --py --sys-prefix


# Getting Started
[![docs](https://readthedocs.org/projects/exa/badge/?version=latest)](https://exa-analytics.github.io/exa/)  
[![gitter](https://badges.gitter.im/exa-analytics/exa.svg)](https://gitter.im/exa-analytics/exa)  

# Development
[![Appveyor](https://ci.appveyor.com/api/projects/status/j6h8pb23xduq5vqs/branch/master?svg=true)](https://ci.appveyor.com/project/avmarchenko/exa/branch/master)
[![Travis](https://travis-ci.org/avmarchenko/exa.svg?branch=master)](https://travis-ci.org/exa-analytics/exa)  
[![Coverage](https://coveralls.io/repos/github/avmarchenko/exa/badge.svg?branch=master)](https://coveralls.io/github/avmarchenko/exa?branch=master)  
[![Codacy](https://api.codacy.com/project/badge/Grade/221e700665c74c85b8255e5b399490d4)](https://www.codacy.com/app/alexvmarch/exa?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=avmarchenko/exa&amp;utm_campaign=Badge_Grade)

For a development ready installation:

    $ git clone https://github.com/avmarchenko/exa.git
    $ cd exa
    $ pip install -e .
    $ cd js
    $ npm install
    $ jupyter nbextension install --py --sys-prefix --symlink exa
    $ jupyter nbextension enable --py --sys-prefix exa 

Note that npm (Node.js) is required. On Windows machines, the ``jupyter nbextension``
commands may need to be run as administrator. After making changes to JavaScript 
extensions:

    $ cd js
    $ npm install

Building the docs requires [sphinx](http://www.sphinx-doc.org/en/stable).
On Linux or Mac OS:

    $ cd js
    $ ./makedocs.sh       # .\makedocs.bat
    $ cd ../docs
    $ make html           # .\make.bat html


# Reference
[![DOI](https://zenodo.org/badge/23807/exa-analytics/exa.svg)](https://zenodo.org/badge/latestdoi/23807/exa-analytics/exa)  


# Legal
[![Apache License 2.0](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0)  
Copyright (c) 2015-2017, Exa Analytics Development Team  
Distributed under the terms of the Apache License 2.0  
