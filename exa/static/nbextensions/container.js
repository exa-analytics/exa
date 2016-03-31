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
    var ContainerView = widget.DOMWidgetView.extend({
        /*"""
        ContainerView
        ===============
        Backbone.js view defined within the ipywidgets JavaScript environment.
        Below is a general outline of the structure of any "View" code.

        Warning:
            Do not override the DOMWidgetView constructor ("initialize").
        */
        render: function() {
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

            this.container.append(this.app.gui.ui.domElement);
            //this.container.append(this.app.gui.ui_css);
            this.setElement(this.container);

        /*    this.init_default_model_listeners();

            this.init_container();                    // Second initialize the
            this.init_canvas();                       // application(s).
            this.app = new app3D.ThreeJSApp(this.canvas);
            console.log($);
            console.log(_);
            console.log(_.object);
            this.send('string');
            this.send(1234);
            this.send([1234, 'package']);
            this.send({'key': 'value', 'key2': 'othervalue'});
            this.send({event: 'stuff'});
            this.send({key: 'stuffsz'});
            //this.app.add_points(this.test_x, this.test_y, this.test_z);

            //this.app.test_mesh();    // Simple box geometry three.app.js test
            //this.app.set_camera();

            this.container.append(this.canvas);       // Lastly set the html
            this.setElement(this.container);          // objects and run.
            this.app.render();
            this.on('displayed', function() {
                self.app.animate();
                self.app.controls.handleResize();
            });*/
        },

        get_trait: function(name) {
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
        },

        set_trait: function(name, value) {
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
        },

        if_test: function() {
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
            console.log(this.app.gui);
        },

        default_listeners: function() {
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
        },

        create_container: function() {
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
        },

        create_canvas: function(shift) {
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
        },

        init_default_model_listeners: function() {
            /*"""
            init_default_model_listeners
            -------------------------------
            Sets up the frontend to listen to common variables present in the
            backend
            */
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


        get_gui_width: function() {
            this.gui_width = this.get_trait('gui_width');
        },

        get_fps: function() {
            this.fps = this.get_trait('fps');
        },

        get_width: function() {
            this.width = this.get_trait('width');
        },

        get_height: function() {
            this.height = this.get_trait('height');
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
