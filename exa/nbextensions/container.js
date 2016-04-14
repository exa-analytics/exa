/*"""
===============
container.js
===============
This module provides custom functionality for communication with the Python
backend via ipywidgets implementation (itself utilizing `backbone.js`_ and
`zeromq`_). It does this via the (extendable) ContainerView class. When
building new data specific notebook widgets, this class should be extended
rather than extending the DOMWidgetView class.

.. _backbone.js: http://backbonejs.org/
.. _zeromq: http://zeromq.org/
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/test.container': {
            exports: 'TestApp'
        },
    },
});


define([
    'widgets/js/widget',
    'nbextensions/exa/test.container'
], function(widget, TestApp) {
    class ContainerView extends widget.DOMWidgetView {
        /*"""
        ContainerView
        ===============
        Base view for creating data specific container widgets used within the
        Jupyter notebook. All logic related to communication (between Python
        and JavaScript) should be located here. This class provides a number
        of commonly used functions for such logic.

        Warning:
            Do not override the DOMWidgetView constructor ("initialize").
        */
        render() {
            /*"""
            render
            -------------
            Main entry point (called immediately after initialize) for
            (ipywidgets) DOMWidgetView objects.

            Note:
                This function  can be overwritten by container specific code,
                but it is more common to overwrite the **init** function.

            See Also:
                **init()**
            */
            this.default_listeners();
            this.create_container();
            this.init();              // Specific to the data container
            this.setElement(this.container);
        };

        init() {
            /*"""
            init
            -------------
            Container view classes that extend this class can overwrite this
            method to customize the behavior of their data specific view.
            */
            this.if_empty();
        };

        get_trait(name) {
            /*"""
            get_trait
            -------------
            Wrapper around the DOMWidgetView (Backbone.js) "model.get" function,
            that attempts to convert JSON strings to objects.
            */
            var obj = this.model.get(name);
            if (typeof obj === 'string') {
                try {
                    obj = JSON.parse(obj);
                } catch(err) {
                    console.log(err);
                };
            };
            return obj;
        };

        set_trait(name, value) {
            /*"""
            set_trait
            ----------
            Wrapper around the DOMWidgetView "model.set" function to correctly
            set json strings.
            */
            if (typeof value === Object) {
                try {
                    value = JSON.stringify(value);
                } catch(err) {
                    console.log(err);
                };
            };
            this.model.set(name, value);
        };

        if_empty() {
            /*"""
            if_empty
            ----------------
            If the (exa) container object is empty, render the test application
            widget.
            */
            var check = this.get_trait('test');
            if (check === true) {
                console.log('Empty container, displaying test interface!');
                this.app = new TestApp(this);
            };
        };

        default_listeners() {
            /*"""
            default_listeners
            -------------------
            Set up listeners for basic variables related to the window dimensions
            and system settings.
            */
            this.get_width();
            this.get_height();
            this.get_gui_width();
            this.get_fps();
            this.get_field_values();
            this.get_field_indices();
            this.listenTo(this.model, 'change:width', this.get_width);
            this.listenTo(this.model, 'change:height', this.get_height);
            this.listenTo(this.model, 'change:gui_width', this.get_gui_width);
            this.listenTo(this.model, 'change:fps', this.get_fps);
            this.listenTo(this.model, 'change:field_values', this.get_field_values);
            this.listenTo(this.model, 'change:field_indices', this.get_field_indices);
        };

        create_container() {
            /*"""
            create_container
            ------------------
            Create a resizable container.
            */
            var self = this;
            this.container = $('<div/>').width(this.width).height(this.height).resizable({
                aspectRatio: false,
                resize: function(event, ui) {
                    self.width = ui.size.width - self.gui_width;
                    self.height = ui.size.height;
                    self.set_trait('width', self.width);
                    self.set_trait('height', self.height);
                    self.canvas.width(self.width);
                    self.canvas.height(self.height);
                    self.app.resize();
                },
            });
        };

        create_canvas() {
            /*"""
            create_canvas
            ----------------
            Create a canvas for WebGL.
            */
            this.canvas = $('<canvas/>').width(this.width - this.gui_width).height(this.height);
            this.canvas.css('position', 'absolute');
            this.canvas.css('top', 0);
            this.canvas.css('left', this.gui_width);
        };

        get_gui_width() {
            this.gui_width = this.get_trait('gui_width');
        };

        get_fps() {
            this.fps = this.get_trait('fps');
        };

        get_width() {
            this.width = this.get_trait('width');
        };

        get_height() {
            this.height = this.get_trait('height');
        };

        get_field_values() {
            this.field_values = this.get_trait('field_values');
        };

        get_field_indices() {
            this.field_indices = this.get_trait('field_indices');
        };
    };

    return {ContainerView: ContainerView};
});
