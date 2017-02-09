// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Abstract Base Classes for Exa Widgets
 * #######################################
 * Every ipywidgets DOMWidget is composed of two JavaScript parts, a model, which
 * describes the data that the widget interacts with from the Python backend, and
 * a view, which defines the visual representation of the model's data. This
 * module provides a default DOMWidgetView that sets up a resizable element with
 * a default stylesheet.
 *
 * @module exa-abcwidgets
 */
"use strict";
var widgets = require("jupyter-js-widgets");


/**
 * Default button class style.
 *
 * @var
 * @type {Object}
 * @default
 * @memberOf exa-abcwidgets
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


var default_style_dict = {
    button: button
};


function compile_css(style_dict) {
    /*"""
    .. function:: compile_css(style_dict)
        
        :param: style_dict: Dict like object containing style tag and value
        :returns: Style element (CSS)
    */
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


// Abstract base view
class ABCView extends widgets.DOMWidgetView {
    /*"""
    ABCView
    ```````````````````````
    An abstract base class for a DOMWidgetView object (the object that actually
    gets rendererd in the browser by the ipywidgets infrastructure).
    */
    render() {
        /*"""
        render
        -----------
        Custom view rendering method that creates a standard widget style.
        To modify the rendering behavior, see the init and launch methods.
        */
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

    init() {
        /*"""
        init
        ---------------
        Abstract method to be modified by the subclass. Called at the start
        of view rendering. Most view specific code belongs here. Interactive
        or app-like widgets can use the launch method, once modifications
        to the view element (here) are complete, to perform additional tasks.
        
        Note:
            This method can modify the css and el attributes as needed.
        */
    }

    launch() {
        /*"""
        launch
        ---------
        Abstract method to be modified by the subclass. Called after the
        init method. Used to start interactive or app like widgets. 
        
        Note:
            No modifications to the view element should be performed here.
        */
    }

    resize(width, height) {
        /*"""
        resize
        ---------------
        Abstract method to be modified by the subclass. Called when the view 
        is resized; resizes any objects with the view (e.g. WebGL contexts, 
        GUI elements).
        */
    }
}


// Abstract base model
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

