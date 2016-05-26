.. _exa-overview:

##################
Overview
##################
Data typically comes as labeled n-dimensional arrays (e.g. comma separated
values). This project organizes data of this type (and
higher dimension data) as parts of a "container". Containers are persistent
data stores for dataframe (spreadsheet like) and series (array like) objects.
For specific applications, custom containers have convenience methods for
processing, analyzing, and visualizing their data.

Containers are designed to be aware of the types of data they contain. The
exa project provides a default container (:class:`~exa.Container`) that is
readily extensible as well as a number of custom built, data specific,
containers. More information about available containers can be found on
the `website`_.

In addition to being a production ready tool for industry, this projects aims
to support academia by enabling transparent, reproducible, scientific data
exploration that can be readily shared between collaborating scientists,
professors, and students.

Technologies
--------------------
This project is built on top of mature, open source, scientific computing
technologies, and is `free as in speech and beer`_. The project uses the Python
as the backend language. All high performance code is written in Python but
`JIT`_ compiled to appropriate, scalable, machine code (CPU, GPU, `GIL`_ free,
etc.). All distributed computing relies on the `MPI`_ library (if available via
the `mpi4py`_ package) with fallback to ssh (`paramiko`_). For high
performance computing centers, this package has support for resource managers
such as `SLURM`_.

User Interfaces
-------------------
This project relies heavily on the `Jupyter notebook`_, an interactive web-based
approach to scientific and technical computing. This interface enables data
exploration, processing, and both 2D and 3D visualization. A second interface,
currently under construction, provides a standalone desktop app.

Usage
--------------------
Within the Jupyter notebook interface, the user is expected to know some
basic Python syntax and be able to issue Python commands. This does not
explicitly require programming knowledge or skills though some basic knowledge
of Python can be very helpful. Additionally, knowledge of `pandas`_ can greatly
improve productivity. The standalone desktop app has less reliance on Python
knowledge, providing what can be a more friendly, but still feature complete,
experience.


.. _website: https://exa-analytics.github.io/
.. _free as in speech and beer: https://en.wikipedia.org/wiki/Gratis_versus_libre
.. _JIT: https://en.wikipedia.org/wiki/Just-in-time_compilation
.. _GIL: https://wiki.python.org/moin/GlobalInterpreterLock
.. _MPI: https://computing.llnl.gov/tutorials/mpi/
.. _paramiko: http://www.paramiko.org/
.. _mpi4py: https://pythonhosted.org/mpi4py/
.. _SLURM: http://slurm.schedmd.com/
.. _Jupyter notebook: https://try.jupyter.org/
.. _pandas: http://pandas.pydata.org/
