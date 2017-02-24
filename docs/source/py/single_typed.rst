.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

########################
Metaclasses
########################
Certain aspects of Exa require static typing and singleton behavior. These
modules provide metaclasses (a definition of a class object - 'the class of a
class') that accomplish these requirements. In general these objects are not
used by users, but rather by developers extending the Exa framework.

.. automodule:: exa.single
    :members:

.. automodule:: exa.typed
    :members:

.. automodule:: exa.tests.test_single
    :members:

.. automodule:: exa.tests.test_typed
    :members:
