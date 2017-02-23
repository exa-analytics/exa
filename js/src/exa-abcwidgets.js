// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * @namespace abcwidgets
 * @desc
 * Every ipywidgets JavaScript widget (DOMWidget) is composed of a model, which
 * describes the data that the widget interacts with from the Python backend, 
 * and a view, which defines the visual representation of the model's data. This
 * namespace provides a default DOMWidgetView that sets up a resizable element 
 * with a default stylesheet.
 *
 * .. note::
 *
 *     The terms module and namespace are used interchangeably.
 */
"use strict";
var widgets = require("jupyter-js-widgets");


/**
 * Default style for HTML buttons.
 * @memberof abcwidgets
 */
var button = {
    "background-color": "grey",
    "border": "1px",
    "color": "black",
    "text-align": "center",
    "font-size": "16px",
    "opacity": "0.5",
    "width": "100px",
    "height": "50px"
};


/**
 * Default styles for all HTML elements.
 */
var default_style_dict = {
    button: button
};


/**
 * Compiles a dict-like object of style parameters into a style element.
 */
function compile_css(style_dict) {
    if (style_dict === undefined) {
        style_dict = default_style_dict;
    };
    var css = "";
    for (var cls in style_dict) {
        if (style_dict.hasOwnProperty(cls)) {
            css += "." + String(cls) + " {\n";
            var style = style_dict[cls];
            for (var sty in style) {
                if (style.hasOwnProperty(sty)) {
                    css += sty + ": " + String(style[sty]) + ";\n";
                }
            }
            css += "}";
        }
    }
    var style = document.createElement("style");
    style.innerHTML = css;
    return style;
}


/**
 * Abstract base class for views.
 *
 * An abstract base class for a DOMWidgetView object (the object that actually
 * gets rendererd in the browser by the ipywidgets infrastructure).
 *
 * @memberof abcwidgets
 */
class ABCView extends widgets.DOMWidgetView {
    /**
     * Render the view.
     *
     * Custom view rendering method that creates a standard widget style.
     * To modify the rendering behavior, see the init and launch methods.
     */
    render() {
        var self = this;
        this.el = $("<div/>").width(this.model.get('width')).height(this.model.get('height')).resizable({
            aspectRatio: false,
            resize: function(event, ui) {
                var w = ui.size.width;
                var h = ui.size.height;
                self.model.set('width', w);
                self.model.set('height', h);
                self.el.width = w;
                self.el.height = h;
                self.resize(w, h);
            }
        });
        this.style_dict = default_style_dict;
        console.log(this.style_dict);
        this.init();
        this.style = compile_css(this.style_dict);
        console.log(this.style)
        this.el.append(this.style);
        this.setElement(this.el);
        this.launch();
    }

    /**
     * Perform setup actions prior to setting the view element.
     *
     * An abstract method to be modified by the subclass. Called at the start
     * of view rendering. Most view specific code belongs here. Interactive
     * or app-like widgets can use the launch method, once modifications
     * to the view element (here) are complete, to perform additional tasks.
     *
     * Note:
     *     This method can modify the css and el attributes as needed.
     */
    init() {
    }

    /**
     * Launches any interactive applications running in the view after setting
     * the view element. 
     *
     * An abstract method to be modified by the subclass. Called after the init
     * method. Used to start interactive or app like widgets. 
     *
     * Note:
     *     No modifications to the view element should be performed here.
     */
    launch() {
    }

    /**
     * Resize any content that has been added to the dynamic view element.
     *
     * An abstract method to be modified by the subclass. Called when the 
     * view is resized; resizes any objects with the view (e.g. WebGL 
     * contexts, GUI elements).
     */
    resize(width, height) {
    }
}


/**
 * Abstract base class for models.
 *
 * An abstract base class for a DOMWidgetModel object (the object that 
 * defines communication between the JavaScript frontend and Python
 * backend (using the ipywidgets infrastructure).
 *
 * @memberof abcwidgets
 */
class ABCModel extends widgets.DOMWidgetModel {
    get defaults() {
        return _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
            _view_name: "ABCView",
            _model_name: "ABCModel",
            _view_name: "jupyter-exa",
            _model_module: "jupyter-exa",
            width: 650,
            height: 400
        });
    }
}


module.exports = {
    "ABCView": ABCView,
    "ABCModel": ABCModel,
    "compile_css": compile_css,
    "default_style_dict": default_style_dict,
    "button": button,
};

