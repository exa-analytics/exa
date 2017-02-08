.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0


########################
Editors
########################
Editors provide a programmatic mechanism for manipulating data files on disk.
For users it can be a convenient way to clean (pre-process data), especially
for common formats such as CSV (for which a convenience class is provided). For
developers, editors provide an easy mechanism for parsing data files into
container objects. Additionally editors are the primary mechanism for
transforming container objects to objects on disk for 3rd party computational
tools (e.g. distributed machine learning).

.. automodule:: exa.core.editor
    :members:

.. automodule:: exa.core.ssv
    :members:
