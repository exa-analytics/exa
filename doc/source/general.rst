Code Overview
======================================
The exa package provides the foundation for data analysis tools. It's primary
purpose is to provide analytical data objects (:mod:`~exa.analytical`), numerical
data objects (:mod:`~exa.numerical`), visualization support (:mod:`~exa.widget`
and :mod:`~exa.web`, for the Jupyter notebook and standalone application
environments respectively), and a container object (itself composed of two
modules, :mod:`~exa.container` and :mod:`~exa.relational.container`) to
facilitate data management and analysis. The secondary purpose of the package
is to provide convenient methods for programmatic analysis and manipulation of
data on disk into analytical and numerical data objects as well as container
objects (:mod:`~exa.editor`). Finally, the exa package provides a set of fast
algorithms (see the modules in the algorithms documentation) for common operations.


Organization
---------------------

Core Functionality
~~~~~~~~~~~~~~~~~~~~~~~
* analytical
* numerical
* widget
* editor
* container

Relational
~~~~~~~~~~~~~~~~
* base
* error
* container
* constant
* unit
* isotope

Algorithms
~~~~~~~~~~~~~~~~~
* broadcasting
* indexing
* iteration

Support
~~~~~~~~~~~~~~~~~~~~~~
* _config
* _install
* error
* log
* test
* utility


Examples
------------------
The package provides a few classes that can be inherited for data specific
applications.

Container
~~~~~~~~~~~~~
Sub-classing a container requires inheriting a `SQLAlchemy`_ model class which
is not always straight forward. The base container object is `polymorphic`_,
therefore when inheriting it, one must add a polymorphic identity to the newly
created container object (**__mapper_args__**). By default, the (SQL) table
name is the lowercase name of the container class (e.g. "container", "universe",
etc.).


.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _polymorphic: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html

.. code-block:: python

    from sqlalchemy import Column, Integer, ForeignKey  # Relational imports
    from exa import Container                           # Import the inheritable container


    class MyContainer(Container):
        '''
        Make sure to add a docstring describing the purpose of this container.
        '''
        mcid = Column(Integer, ForeignKey('container.pkid'), primary_key=True)  # Relationship to the original container
        other_column = Column(...)
        __mapper_args__ = {'polymorphic_identity': 'mycontainer'}               # Polymorphic table name

        def __init__(self, section1, section2, **kwargs):
            super().__init__(**kwargs)    # Don't forget this line or the kwargs!
            self.section1 = section1
            self.section2 = section2


Numerical Data Objects
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from exa import Series

    class MySeries(Series):
        '''
        MySeries class description
        '''
        pass


.. code-block:: python

    from exa import DataFrame

    class MyDataFrame(DataFrame):
        '''
        '''
        _indices = ['myindex']               # Required index name
        _columns = ['x', 'y', 'group', 'c']  # Required column names
        _traits = ['x', 'y']                 # Columns that are passed to the frontend
        _groupbys = ['group']                # Columns by which to group the data
        _categories = {'c': str}             # Columns that are categories and their original type

        @classmethod
        def custom_constructor(cls, arg):
            '''
            Custom construction of this dataframe from a specific arg.

            Args:
                arg (type): Specific arg

            Returns:
                df (MyDataFrame): Custom dataframe from specific arg
            '''
            arg *= arg
            return cls(arg)


Editor
~~~~~~~~~~~~~~~~~
Inheriting the editor can be done as follows.

.. code-block:: python

    from exa import Editor

    class SectionFile(Editor):
        '''
        My custom editor
        '''
        def parse_section1(self):
            '''
            Parses section1 of the section file
            '''
            pass

        def parse_section2(self):
            pass

        def to_container(self):
            '''
            Create the corresponding container for this editor
            '''
            return MyContainer(section1=self.parse_section1(),
                               section2=self.parse_section2())
