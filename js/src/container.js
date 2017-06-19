// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
=================
container.js
=================
JavaScript "frontend" complement of exawidget's Container for use within
the Jupyter notebook interface. This "module" standardizes bidirectional
communication logic for all container widget views.

The structure of the frontend is to generate an HTML widget ("container" - see
create_container) and then populate its canvas with an application ("app")
appropriate to the type of container. If the (backend) container is empty, then
populate the HTML widget with the test application.
*/
"use strict";
var widgets = require("jupyter-js-widgets");
var THREE = require("three");
var $ = require("jquery");
require("jquery-ui");
var _ = require("underscore");
var TestApp = require("./test.js").TestApp;

// var BaseDOMModel = widgets.DOMWidgetModel.extend({
//     defaults: function() {
//         return _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
//             _model_module: "jupyter-exawidgets",
//             _view_module: "jupyter-exawidgets",
//             _model_name: "BaseDOMModel",
//             _view_name: "BaseDOMView"
//         });
//     }
// });
//
// var BaseDOMView = widgets.DOMWidgetView.extend({
// });
//
// var GUIModel = BaseDOMModel.extend({
//     defaults: function() {
//         return _.extend(BaseDOMModel.prototype.defaults(), {
//             _model_name: "GUIModel",
//             _view_name: "GUIView",
//             width: "250"
//         });
//     }
// }, {
//     serializers: _.extend({
//         button: { deserialize: widgets.unpack_models }
//     }, BaseDOMModel.serializers)
// });
//
// var GUIView = BaseDOMView.extend({
// });
//
// var SceneModel = BaseDOMModel.extend({
//     defaults: function() {
//         return _.extend(BaseDOMModel.prototype.defaults(), {
//             _model_name: "SceneModel",
//             _view_name: "SceneView",
//         });
//     }
// });
//
// var SceneView = BaseDOMView.extend({
// });
//
// var ContainerModel = BaseDOMModel.extend({
//     defaults: function() {
//         return _.extend(BaseDOMModel.prototype.defaults(), {
//             _model_name: "ContainerModel",
//             _view_name: "ContainerView",
//             scene: undefined,
//             gui: undefined
//         });
//     }
// }, {
//     serializers: _.extend({
//         gui: { deserialize: widgets.unpack_models },
//         scene: { deserialize: widgets.unpack_models }
//     }, BaseDOMModel.serializers)
// });
//
// var ContainerView = BaseDOMView.extend({
//
//     initialize: function() {
//         this.el.classList.add("jupyter-exawidgets");
//         this.el.classList.add("container");
//         this.el.classList.add("jupyter-widgets");
//         var gui_width = this.model.get("gui").get("width");
//         var height = this.model.get("layout").get("height");
//         var width = this.model.get("layout").get("width");
//         var scene = document.createElement("div");
//         var gui = document.createElement("div");
//         gui.style.background_color = "black";
//         this.el.appendChild(gui);
//         this.el.appendChild(scene);
//         $(this.el.gui).width(gui_width).height(height);
//         $(this.el.scene).width(width - gui_width).height(height);
//         console.log($(this.el.gui));
//         console.log(this.el);
//         //var scene = $("<div/>").width(width - gui_width).height(height);
//         console.log(gui);
//         console.log(gui.style);
//         //gui.style.width = this.model.get("gui").get("width");
//         //gui.style.background_color = "black";
//         //console.log(gui.style);
//         //scene.style.left = this.model.get("gui").get("width");
//         //console.log(gui);
//         var that = this;
//         $(this.el).width(
//             this.model.get("layout").get("width") - this.model.get("gui").get("width")).height(
//             this.model.get("layout").get("height")).resizable({
//             aspectRatio: false,
//             resize: function(event, ui) {
//                 var w = ui.size.width;
//                 var h = ui.size.height;
//                 that.model.get("layout").set('width', w);
//                 that.model.get("layout").set('height', h);
//                 that.el.width = w;
//                 that.el.height = h;
//             }
//         });
//         ContainerView.__super__.initialize.apply(this, arguments);
//     },
//
//     render: function() {
//         this.gui_width = this.model.get("gui").get("width");
//         this.width = this.model.get("layout").get("width");
//         this.height = this.model.get("layout").get("height");
//         var that = this;
//         console.log(this.$el);
//         console.log(this.gui_width);
//         console.log(this.width);
//         console.log(this.height);
//         console.log(this);
//         var that = this;
//     }
// });

class BaseModel extends widgets.DOMWidgetModel {
    get defaults() {
      return _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
            _model_module: "jupyter-exawidgets",
            _view_module: "jupyter-exawidgets",
            _model_name: "BaseModel",
            _view_name: "BaseView",
            width: 800,
            height: 500
        });
    }
}

class BaseView extends widgets.DOMWidgetView {

}

class ContainerModel extends BaseModel {
    get defaults() {
      return _.extend({}, BaseModel.prototype.defaults, {
            _model_module: "jupyter-exawidgets",
            _view_module: "jupyter-exawidgets",
            _model_name: "ContainerModel",
            _view_name: "ContainerView",
            gui_width: 250,
        });
    }
}

class ContainerView extends BaseView {
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
        if (typeof obj === "string") {
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
        var check = this.get_trait("test");
        if (check === true) {
            console.log("Empty container, displaying test interface!");
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
        this.listenTo(this.model, "change:width", this.get_width);
        this.listenTo(this.model, "change:height", this.get_height);
        this.listenTo(this.model, "change:gui_width", this.get_gui_width);
        this.listenTo(this.model, "change:fps", this.get_fps);
        this.listenTo(this.model, "change:field_values", this.get_field_values);
        this.listenTo(this.model, "change:field_indices", this.get_field_indices);
    };

    create_container() {
        /*"""
        create_container
        ------------------
        Create a resizable container.
        */
        var self = this;
        this.container = $("<div/>").width(this.width).height(this.height).resizable({
            aspectRatio: false,
            resize: function(event, ui) {
                self.width = ui.size.width - self.gui_width;
                self.height = ui.size.height;
                self.set_trait("width", self.width);
                self.set_trait("height", self.height);
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
        this.canvas = $("<canvas/>").width(this.width - this.gui_width).height(this.height);
        this.canvas.css("position", "absolute");
        this.canvas.css("top", 0);
        this.canvas.css("left", this.gui_width);
    };

    get_gui_width() {
        this.gui_width = this.get_trait("gui_width");
    };

    get_fps() {
        this.fps = this.get_trait("fps");
    };

    get_width() {
        this.width = this.get_trait("width");
    };

    get_height() {
        this.height = this.get_trait("height");
    };

    get_field_values() {
        this.field_values = this.get_trait("field_values");
    };

    get_field_indices() {
        this.field_indices = this.get_trait("field_indices");
    };
};

module.exports = {
    BaseModel: BaseModel,
    BaseView: BaseView,
    //BaseDOMModel: BaseDOMModel,
    //BaseDOMView: BaseDOMView,
    //GUIModel: GUIModel,
    //GUIView: GUIView,
    //SceneModel: SceneModel,
    //SceneView: SceneView,
    ContainerView: ContainerView,
    ContainerModel: ContainerModel
}
