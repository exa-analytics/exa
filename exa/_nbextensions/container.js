/*"""
container.js
###############
JavaScript "frontend" counterpart of exa's Container object for use within
the Jupyter notebook interface. This "module" standardizes bidirectional
communication logic for all container widget views.

The structure of the frontend is to generate an HTML widget ("container" - see
create_container) and then populate its canvas with an application ("app")
appropriate to the type of container. If the (backend) container is empty, then
populate the HTML widget with the test application. If the container is not
empty but doesn't have a dedicated application, the info application (info.js)
is used.*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/test': {
            exports: 'TestApp'
        },
        'nbextensions/exa/info': {
            exports: 'InfoApp'
        }
    },
});


// THIS WILL HAVE TO CHANGE with updates to ipywidgets and notebook packages
// define('ContainerView', ["jupyter-js-widgets"], function(widgets) {})
define([
    'widgets/js/widget',
    'nbextensions/exa/test',
    'nbextensions/exa/info'

], function(widget, TestApp, InfoApp) {
    class ContainerView extends widget.DOMWidgetView {
        /*"""
        ContainerView
        ===============
        JavaScript counterpart for exa's ContainerWidget.
        */
        render() {
            /* Method is automatically called first and sets up the canvas and
               elements which will be drawn in the widget. */
            this.default_listeners();    // Set up default listeners
            this.create_container();     // Create the widget HTML container
            this.default_app = InfoApp;
            this.init();                 // Populate the HTML container with an "app"
            this.setElement(this.container);
        };

        init() {
            // If test container run test app other run default application
            var test = this.model.get('test');
            if (test === true) {
                this.app = new TestApp(this);
            } else {
                this.app = new this.default_app(this);
            };
        };

        get_trait(name) {
            /*"""
            get_trait
            -------------
            Wrapper around the DOMWidgetView (Backbone.js) "model.get" function,
            that attempts to convert JSON strings to Object(s).
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

        default_listeners() {
            // Default backend variable listeners
            this.get_width();
            this.get_height();
            this.get_gui_width();
            this.get_fps();
            //this.get_field_values();
            //this.get_field_indices();
            this.listenTo(this.model, 'change:width', this.get_width);
            this.listenTo(this.model, 'change:height', this.get_height);
            this.listenTo(this.model, 'change:gui_width', this.get_gui_width);
            this.listenTo(this.model, 'change:fps', this.get_fps);
            //this.listenTo(this.model, 'change:field_values', this.get_field_values);
            //this.listenTo(this.model, 'change:field_indices', this.get_field_indices);
        };

        create_container() {
            // Create a resizable HTML container for the widget
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
            // Helper for creating a 3D rendering canvas
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
