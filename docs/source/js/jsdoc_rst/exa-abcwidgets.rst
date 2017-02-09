

exa-abcwidgets
==============

.. code-block:: js

    var module = require('exa-abcwidgets')

Abstract Base Classes for Exa Widgets
#######################################
Every ipywidgets DOMWidget is composed of two JavaScript parts, a model, which
describes the data that the widget interacts with from the Python backend, and
a view, which defines the visual representation of the model's data. This
module provides a default DOMWidgetView that sets up a resizable element with
a default stylesheet.



.. currentmodule:: exa-abcwidgets

.. data:: button

    Default button class style.

    :type: Object
    :default: {"undefined":"50px"}



