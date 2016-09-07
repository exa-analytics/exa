[![exa logo](doc/source/_static/logo.png)](https://exa-analytics.github.io)  

Installation
===================
[![conda Badge](https://anaconda.org/exaanalytics/exa/badges/installer/conda.svg)](https://conda.anaconda.org/exaanalytics)  
[![pypi badge](https://badge.fury.io/py/exa.svg)](https://badge.fury.io/py/exa)  
Exa is available through [anaconda](https://www.continuum.io/downloads)  
```
conda install -c exaanalytics exa
```
or [pypi](https://pypi.python.org/pypi)
```
pip install exa
jupyter nbextension enable --py --sys-prefix exa
```

Getting Started
==================
[![readthedocs](https://readthedocs.org/projects/exa/badge/?version=latest)](http://exa.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://badges.gitter.im/exa-analytics/exa.svg)](https://gitter.im/exa-analytics/exa)

Building the docs requires [sphinx](http://www.sphinx-doc.org/en/stable)
```
cd doc
make html    # `.\make.bat html` on windows
```

Development
=================
[![travis](https://travis-ci.org/exa-analytics/exa.svg?branch=master)](https://travis-ci.org/exa-analytics/exa)
[![codecov](https://codecov.io/gh/exa-analytics/exa/branch/master/graph/badge.svg)](https://codecov.io/gh/exa-analytics/exa)
[![quantcode](https://www.quantifiedcode.com/api/v1/project/3c8a5fe969f745f8b2f3554ad59590f0/badge.svg)](https://www.quantifiedcode.com/app/project/3c8a5fe969f745f8b2f3554ad59590f0)
Note that development requires [npm](https://nodejs.org/en/).
```
git clone https://github.com/exa-analytics/exa.git
cd exa
pip install -e .
jupyter nbextension install --py --symlink --sys-prefix exa
jupyter nbextension enable --py --sys-prefix exa
```
.
+-- data (example data)
|   +-- stuff
|   +-- things
+-- exa  (Python package dir)
+-- examples (Jupyter notebooks)
+-- js (Custom Jupyter notebook widget JavaScript)
+-- paper (Academic paper)
+-- static (Web application static code)
+-- templates (Web app templates)


Legal
========
[![Apache License 2.0](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0)
Copyright (c) 2015-2016, Exa Analytics Development Team
Distributed under the terms of the Apache License 2.0
