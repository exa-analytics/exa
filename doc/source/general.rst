Code Overview
======================================
The exa package provides the foundation for data analysis tools. It's primary
purpose is to provide **analytical** data objects (:mod:`~exa.analytical`), **numerical**
data objects (:mod:`~exa.numerical`), **visualization** support (:mod:`~exa.widget`
and :mod:`~exa.web` - for both the **Jupyter notebook** and standalone application
environments), and a **container** object (itself composed of two
modules, :mod:`~exa.container` and :mod:`~exa.relational.container`) to
facilitate data **management** and **analysis**. The secondary purpose of the package
is to provide convenient methods for **programmatic analysis** and manipulation of
data on disk into analytical and numerical data objects as well as container
objects (:mod:`~exa.editor`). Finally, the exa package provides a set of fast
(in and out of core) **algorithms** (see the modules in the algorithms
documentation) for common operations.

The latter two purposes are accomplished in practice by using data specific
packages built on top of exa; exa provides the foundation for manipulation of
n-dimensional data, communication to data frameworks, databases, data transfer
between programming languages (i.e. frontend and backend), and content
management.

Note:
    Performance is critical for such applications both in terms of speed and memory
    usage. The backend application is built exclusively in **Python**: Python has well
    established libraries for accomplishing all of the foundational task described
    above. **JavaScript/HTML/CSS** are used for creating dynamic Jupyter notebook
    extensions, and are also used for the standalone web application. Other languages,
    primarily **C++**, are used for situations requiring high performance.

Tip:
    Due to the limitations of Python and JavaScript, numerically difficult operations
    should be offloaded to statically typed languages (or use numpy for example).
    Where unavoidable every effort should be made to not waste cpu cycles or memory.
    Whenever communication is required between languages, ensure that only the
    minimum amount of data is being copied and/or transferred.

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


Python Sub-classing
----------------------
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

JavaScript Extensions
----------------------
In order to support data container specific visualization within the Jupyter notebook
environment, extensions must be written. The base package (exa) handles communication
between the frontend JavaScript application and backend Python dataframe objects. It
also provides a two interfaces to 3D and 2D rendering applications on which the data
specific visualization application can be built.

Below is an example application for a data container containing dataframes with
information about atoms' coordinates, types, and their electronic densities. The
data container is called a Universe; the corresponding JavaScript, universe.js,
handles communication between the frontend and backend (akin to container.js).
The application JavaScript, app.js, builds a custom graphical user interface for
interacting with this specific application.

universe.js
~~~~~~~~~~~~~~

.. code-block:: javascript

    // container is a require.js reference to container.js
    var UniverseView = container.ContainerView.extend({
        render: function() {
            console.log('Initializing universe...');
            this.model.one('change:atom_x', this.update_atom_x, this);
            this.update_atom_x();
            this.init_canvas();
            console.log(this.atom_x);
        },

        update_atom_x: function() {
            this.atom_x = this.get_traits('atom_x');    // provided by container.js
        },
    });


app.js
~~~~~~~~~~~~~~~~

.. code-block:: javascript

    var AtomicApp = function(view) {
        this.view = view;    // reference to instance of UniverseView (above);
        this.canvas = this.view.canvas;
        this.index = 0;
        this.app3d = new app3D.ThreeJSApp(this.canvas);    // provided by three.app.js
        this.gui = new dat.GUI({autoPlace: false, width: this.view.gui_width});
        this.gui_style = document.createElement('style');
        this.gui_style.innerHTML = gui_style;
        this.init_gui();
        this.render_atoms(this.index);
    };
