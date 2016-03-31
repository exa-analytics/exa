/*"""
===============
container.js
===============
This module provides custom functionality for communication with the Python
backend via ipywidgets implementation (itself utilizing `backbone.js`_ and
`zeromq`_).

.. _backbone.js: http://backbonejs.org/
.. _zeromq: http://zeromq.org/
*/
'use strict';

require.config({
    shim: {
        'nbextensions/exa/test': {
            exports: 'test'
        },
    },
});

define([
    'widgets/js/widget',
    'nbextensions/exa/test'
], function(widget, test) {
    class ContainerView extends widget.DOMWidgetView {
        /*"""
        ContainerView
        ===============
        Backbone.js view defined within the ipywidgets JavaScript environment.
        Below is a general outline of the structure of any "View" code.

        Warning:
            Do not override the DOMWidgetView constructor ("initialize").
        */
        render() {
            /*"""
            render
            -------------
            Main entry point (called immediately after initialize) for
            ipywidgets DOMWidgetView objects.

            Note:
                This function is typically overwritten by data specific packages.
            */
            var self = this;
            console.log('Initializing container view...');
            this.default_listeners();
            this.create_container();
            this.create_canvas();
            this.if_test();

            this.container.append(this.app.gui.domElement);
            this.container.append(this.app.gui.ui_css);
            this.setElement(this.container);
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

        if_test() {
            /*"""
            if_test
            ----------------
            If this is an empty container we display demo/test features.

            This testing application allows us to test all of the basic features
            of this container object and sends the results back to Python for
            logging.
            */
            var check = this.get_trait('test');
            if (check === true) {
                console.log('Empty container, displaying test interface!');
            };
            this.app = new test.TestApp(this);
            console.log(this.app);
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
            this.listenTo(this.model, 'change:width', this.get_width);
            this.listenTo(this.model, 'change:height', this.get_height);
            this.listenTo(this.model, 'change:gui_width', this.get_gui_width);
            this.listenTo(this.model, 'change:fps', this.get_fps);
            console.log(this.width);
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

        create_canvas(shift) {
            /*"""
            create_canvas
            ----------------
            Create a canvas for WebGL.
            */
            shift = shift || 0;     // default shift
            this.canvas = $('<canvas/>').width(this.width - shift).height(this.height);
            this.canvas.css('position', 'absolute');
            this.canvas.css('top', 0);
            this.canvas.css('left', shift);
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
    };

    return {'ContainerView': ContainerView};
});
