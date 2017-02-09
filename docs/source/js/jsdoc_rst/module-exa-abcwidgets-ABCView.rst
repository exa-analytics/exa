.. _module-exa-abcwidgets.ABCView:

==================
Class: ``ABCView``
==================

Member Of :doc:`module-exa-abcwidgets`

.. contents:: Local Navigation
   :local:

Children
========

.. toctree::
   :maxdepth: 1
   
   
Description
===========




.. _module-exa-abcwidgets-ABCView.render:


Function: ``render``
====================

Render the view.

Custom view rendering method that creates a standard widget style.
To modify the rendering behavior, see the init and launch methods.

.. js:function:: render()

    
    
.. _module-exa-abcwidgets-ABCView.init:


Function: ``init``
==================

Perform setup actions prior to setting the view element.

An abstract method to be modified by the subclass. Called at the start
of view rendering. Most view specific code belongs here. Interactive
or app-like widgets can use the launch method, once modifications
to the view element (here) are complete, to perform additional tasks.

Note:
    This method can modify the css and el attributes as needed.

.. js:function:: init()

    
    
.. _module-exa-abcwidgets-ABCView.launch:


Function: ``launch``
====================

Launches any interactive applications running in the view after setting
the view element. 

An abstract method to be modified by the subclass. Called after the init
method. Used to start interactive or app like widgets. 

Note:
    No modifications to the view element should be performed here.

.. js:function:: launch()

    
    
.. _module-exa-abcwidgets-ABCView.resize:


Function: ``resize``
====================

Resize any content that has been added to the dynamic view element.

An abstract method to be modified by the subclass. Called when the 
view is resized; resizes any objects with the view (e.g. WebGL 
contexts, GUI elements).

.. js:function:: resize()

    
    

.. _module-exa-abcwidgets-ABCView.el:

Member: ``el``: 

.. _module-exa-abcwidgets-ABCView.style_dict:

Member: ``style_dict``: 

.. _module-exa-abcwidgets-ABCView.style:

Member: ``style``: 




