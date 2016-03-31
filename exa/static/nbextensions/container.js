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

            Note:
                This function is typically overwritten by data specific packages.
            */
            console.log('Initializing container...');
            var self = this;                          // First pull in the data
            this.init_default_model_listeners();
            this.update_x();
            this.update_y();
            this.update_z();
            this.model.on('change:test_x', this.update_x, this);
            this.model.on('change:test_y', this.update_y, this);
            this.model.on('change:test_z', this.update_z, this);

            this.init_container();                    // Second initialize the
            this.init_canvas();                       // application(s).
            this.app = new app3D.ThreeJSApp(this.canvas);
            this.app.add_points(this.test_x, this.test_y, this.test_z);

            //this.app.test_mesh();    // Simple box geometry three.app.js test
            this.app.set_camera();

            this.container.append(this.canvas);       // Lastly set the html
            this.setElement(this.container);          // objects and run.
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
                    self.width = ui.size.width - self.gui_width;
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
            shift = shift || 0;     // default shift
            this.canvas = $('<canvas/>').width(this.width - shift).height(this.height);
            this.canvas.css('position', 'absolute');
            this.canvas.css('top', 0);
            this.canvas.css('left', shift);
        },

        init_default_model_listeners: function() {
            /*"""
            init_default_model_listeners
            -------------------------------
            Sets up the frontend to listen to common variables present in the
            backend
            */
            this.field_values = {};    // Works like a Python dictionary
            this.update_width();
            this.update_height();
            this.update_gui_width();
            this.update_fps();
            this.update_field_nx();
            this.update_field_ny();
            this.update_field_nz();
            this.update_field_xi();
            this.update_field_xj();
            this.update_field_xk();
            this.update_field_yi();
            this.update_field_yj();
            this.update_field_yk();
            this.update_field_zi();
            this.update_field_zj();
            this.update_field_zk();
            this.update_field_ox();
            this.update_field_oy();
            this.update_field_oz();
            this.update_field_values();
            this.update_field_indices();
            this.model.on('change:width', this.update_width, this);
            this.model.on('change:height', this.update_height, this);
            this.model.on('change:gui_width', this.update_gui_width, this);
            this.model.on('change:fps', this.update_fps, this);
            this.model.on('change:field_nx', this.update_field_nx, this);
            this.model.on('change:field_ny', this.update_field_ny, this);
            this.model.on('change:field_nz', this.update_field_nz, this);
            this.model.on('change:field_xi', this.update_field_xi, this);
            this.model.on('change:field_xj', this.update_field_xj, this);
            this.model.on('change:field_xk', this.update_field_xk, this);
            this.model.on('change:field_yi', this.update_field_yi, this);
            this.model.on('change:field_yj', this.update_field_yj, this);
            this.model.on('change:field_yk', this.update_field_yk, this);
            this.model.on('change:field_zi', this.update_field_zi, this);
            this.model.on('change:field_zj', this.update_field_zj, this);
            this.model.on('change:field_zk', this.update_field_zk, this);
            this.model.on('change:field_ox', this.update_field_ox, this);
            this.model.on('change:field_oy', this.update_field_oy, this);
            this.model.on('change:field_oz', this.update_field_oz, this);
            this.model.on('change:field_values', this.update_field_values, this);
            this.model.on('change:field_indices', this.update_field_values, this);
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

        update_gui_width: function() {
            this.gui_width = this.get_trait('gui_width');
        },

        update_fps: function() {
            this.fps = this.get_trait('fps');
        },

        update_width: function() {
            this.width = this.get_trait('width');
        },

        update_height: function() {
            this.height = this.get_trait('height');
        },

        update_x: function() {
            this.test_x = this.get_trait('test_x');
        },

        update_y: function() {
            this.test_y = this.get_trait('test_y');
        },

        update_z: function() {
            this.test_z = this.get_trait('test_z');
        },

        update_field_nx: function() {
            this.field_nx = this.get_trait('field_nx');
        },

        update_field_ny: function() {
            this.field_ny = this.get_trait('field_ny');
        },

        update_field_nz: function() {
            this.field_nz = this.get_trait('field_nz');
        },

        update_field_xi: function() {
            this.field_xi = this.get_trait('field_xi');
        },

        update_field_xj: function() {
            this.field_xj = this.get_trait('field_xj');
        },

        update_field_xk: function() {
            this.field_xk = this.get_trait('field_xk');
        },

        update_field_yi: function() {
            this.field_yi = this.get_trait('field_yi');
        },

        update_field_yj: function() {
            this.field_yj = this.get_trait('field_yj');
        },

        update_field_yk: function() {
            this.field_yk = this.get_trait('field_yk');
        },

        update_field_zi: function() {
            this.field_zi = this.get_trait('field_zi');
        },

        update_field_zj: function() {
            this.field_zj = this.get_trait('field_zj');
        },

        update_field_zk: function() {
            this.field_zk = this.get_trait('field_zk');
        },

        update_field_ox: function() {
            this.field_ox = this.get_trait('field_ox');
        },

        update_field_oy: function() {
            this.field_oy = this.get_trait('field_oy');
        },

        update_field_oz: function() {
            this.field_oz = this.get_trait('field_oz');
        },

        update_field_values: function() {
            this.field_values = this.get_trait('field_values');
            console.log(this.field_values);
        },

        update_field_indices: function() {
            this.field_indices = this.get_trait('field_indices');
            console.log(this.field_indices);
        },
    });

    return {'ContainerView': ContainerView};
});
