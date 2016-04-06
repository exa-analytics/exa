Full Stack Design
======================================
In the graphic below, the technical organization of the code's logic is
described. Specifically, the distribution of communication (between languages)
and structure of GUI related code is given. In a model-view-controller sense
(the model updates the view, the user sees the view, the users interacts with
the controller, the controller manipulates the model, and the cycle repeats),
the model is the (backend) **Python** code, the view is **container.js**,
and the controller is **app.js**. In some cases the controller only
performs aesthetic changes to the view and does not require communication with
the model (note that communication between the controller and model, and model
and view is the most expensive step due to transformation of objects between
languages - usually requiring in memory copies).

.. image:: _static/stack.jpg
