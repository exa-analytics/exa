.. image:: doc/source/_static/logo.png
    :target: doc/source/_static/logo.png
    :alt: Logo

.. image:: https://travis-ci.org/avmarchenko/exa.svg?branch=master
    :target: https://travis-ci.org/avmarchenko/exa
    :alt: Build Status

.. image:: https://readthedocs.org/projects/exa/badge/?version=latest
    :target: http://exa.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://www.quantifiedcode.com/api/v1/project/3c8a5fe969f745f8b2f3554ad59590f0/badge.svg
    :target: https://www.quantifiedcode.com/app/project/3c8a5fe969f745f8b2f3554ad59590f0
    :alt: Code Issues

.. image:: https://codecov.io/gh/avmarchenko/exa/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/avmarchenko/exa
    :alt: Code Coverage

Installation
##################
**Note** conda build coming soon!
The typical Python data stack is required (example using the **conda** package manager).
```
conda install numpy scipy pandas seaborn scikit-learn jupyter notebook ipywidgets sphinx
```
Currently there are some growing pains associated with our dependencies. Ensure that
you have identical version numbers on ipywidgets and jupyter-client (eg. ipywidgets=4.1.1
and jupyter-client=4.1.1).


Getting Started
##################


Documentation
###################
Documentation is generated using [sphinx](http://sphinx-doc.org "Sphinx")
```
cd doc
make html    # .\make.bat html # Windows
```

Legal
###############
Copyright (c) 2015-2016, Exa Analytics Development Team

Distributed under the terms of the Apache License 2.0
