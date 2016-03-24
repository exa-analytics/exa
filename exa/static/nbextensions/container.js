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
        'nbextensions/exa/three.app': {
            exports: 'app3D'
        },

        'nbextensions/exa/utility': {
            exports: 'utility'
        },
    },
});

define([
    'widgets/js/widget',
    'nbextensions/exa/three.app',
    'nbextensions/exa/utility'
], function(widget, app3D, utility) {
    var ContainerView = widget.DOMWidgetView.extend({
        /*"""
        ContainerView
        ===============
        Backbone.js view defined within the ipywidgets JavaScript environment.
        Below is a general outline of the structure of any "View" code.
        */
        render: function() {
            /*"""
            render
            -------------
            Main entry point (called immediately after the constructor) for
            ipywidgets DOMWidgetView objects.
            */
            console.log('Initializing container...');
            var self = this;
            this.model.on('change:width', this.update_width, this);
            this.model.on('change:height', this.update_height, this);
            this.model.on('change:test_3D', this.update_3D, this);
            this.model.on('change:test_2D', this.update_2D, this);
            this.model.on('change:test_diameter', this.update_diameter, this);

            this.update_width();
            this.update_height();

            this.init_canvas();
            this.init_3D(this.canvas);

            this.update_3D();
            this.update_2D();
            this.update_diameter();
            
            this.app.test_mesh();    // Simple box geometry three.app.js test
            this.init_container();
            this.container.append(this.canvas);
            this.setElement(this.container);

            this.app.render();
            this.on('displayed', function() {
                self.app.animate();
                self.app.controls.handleResize();
            });
        },

        init_container: function() {
            /*"""
            init_container
            --------------
            Create a resizable container.
            */
            var self = this;
            this.container = $('<div/>').width(this.width).height(this.height).resizable({
                aspectRatio: false,
                resize: function(event, ui) {
                    self.width = ui.size.width;
                    self.height = ui.size.height;
                    self.set_trait('width', self.width);
                    self.set_trait('height', self.height);
                    self.canvas.width(self.width);
                    self.canvas.height(self.height);
                    self.app.resize();
                },
            });
        },

        init_canvas: function(shift) {
            /*"""
            init_canvas
            -------------
            Create a canvas for WebGL.
            */
            var shift = shift || 0;     // default shift
            this.canvas = $('<canvas/>').width(this.width - shift).height(this.height);
            this.canvas.css('position', 'absolute');
            this.canvas.css('top', 0);
            this.canvas.css('left', shift);
        },

        init_3D: function(canvas) {
            /*"""
            init_3D
            ------------
            Initializes a 3D application (using the three.js backend).

            See Also:
                Documentation for three.app.js (below).
            */
            this.app = new app3D.ThreeJSApp(canvas);
        },

        app3D_displayed: function() {
            /*"""
            app3D_displayed
            ------------------
            Should be run when backbone returns the displayed status if using
            the 3D app.
            */
            this.app.animate();
            this.app.controls.handleResize();
        },

        get_trait: function(name) {
            /*"""
            get_trait
            -------------
            Wrapper around the DOMWidgetView (Backbone.js) "model.get" function,
            that attempts to convert JSON strings to objects. Note that
            */
            var obj = this.model.get(name);
            if (typeof obj == 'string') {
                try {
                    obj = JSON.parse(obj);
                } catch(err) {
                    console.log(err);
                };
            };
            return obj;
        },

        set_trait: function(name, value) {
            /*"""
            set_trait
            ----------
            Wrapper around the DOMWidgetView "model.set" function to correctly
            set json strings.
            */
            if (typeof value == 'Object') {
                try {
                    value = JSON.stringify(value);
                } catch(err) {
                    console.log(err);
                };
            };
            this.model.set(name, value);
        },

        update_width: function() {
            /*"""
            update_width
            -----------------
            Updates widget width.
            */
            this.width = this.get_trait('width');
        },

        update_height: function() {
            /*"""
            update_height
            -----------------
            Updates widget height.
            */
            this.height = this.get_trait('height');
        },

        update_3D: function() {
            /*"""
            update_3D
            ------------
            Update the frontend value of the 3D array
            */
            this.value3D = this.get_trait('test_3D');
            this.app.add_spheres(this.value3D);
        },

        update_2D: function() {
            /*"""
            update_2D
            ------------
            Update the frontend value of the 2D array
            */
            this.value2D = this.get_trait('test_2D');
        },

        update_diameter: function() {
            /*"""
            update_3D
            ------------
            Update the frontend value of the 3D array
            */
            this.diameter = this.get_trait('test_diameter');
        },
    });

    return {'ContainerView': ContainerView};
});
