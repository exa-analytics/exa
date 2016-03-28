NBExtensions
==============
*Jupyter notebook extensions written in JavaScript.*

This code relies on the `ipywidgets`_ package (and the dependencies therein). Every (Python)
data container has a corresponding visualization application. This application typically
consists of a few parts, one piece of code which handles communication between the frontend
and backend, and another piece of code which handles communication between the frontend and
third-party JavaScript libraries on which the application is built.

This package provides some foundational communication support (see **container.js**) as
well as support for a couple of commonly used libraries for building applications
(see **three.app.js** and **two.app.js**) and some utility functions (**utility.js**).

.. autoanysrc:: directives
    :src: ../../exa/static/nbextensions/container.js
    :analyzer: js

.. autoanysrc:: directives
    :src: ../../exa/static/nbextensions/three.app.js
    :analyzer: js

.. autoanysrc:: directives
    :src: ../../exa/static/nbextensions/utility.js
    :analyzer: js

.. _ipywidgets: http://ipywidgets.readthedocs.org/en/latest/
