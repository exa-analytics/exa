// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * This module provides the base model and view used by
 * exa.core.widget.DOMWidget.
 * @module
 */
"use strict";
var ipywidgets = require("jupyter-js-widgets");
var _ = require("underscore");
var three = require("three");
three.TrackballControls = require("three-trackballcontrols");
console.log(three);


/**
 * Model class for all "Exa" DOMWidgets.
 */
class DOMWidgetModel extends ipywidgets.DOMWidgetModel {
    /**
     * Get the default class values.
     * Used by jupyter-js-widgets.
     */
    get defaults() {
        return _.extend({}, ipywidgets.DOMWidgetModel.prototype.defaults, {
            _view_name: "DOMWidgetView",
            _view_module: "jupyter-exa",
            _view_module_version: "^0.4.0",
            _model_name: "DOMWidgetModel",
            _model_module: "jupyter-exa",
            _model_module_version: "^0.4.0"
        });
    }
}


/**
 * View class for all "Exa" DOMWidgets.
 */
class DOMWidgetView extends ipywidgets.DOMWidgetView {
}


class ModelTemplate extends DOMWidgetModel {
    constructor(name, fn) {
        console.log("creating: " + name);
        this.model_name = name + "Model";
        this.view_name = name + "View";
        this.fn = fn;
    }

    get defaults() {
        return _.extend({}, DOMWidgetModel.prototype.defaults, {
            _view_name: this.view_name,
            _model_name: this.model_name
        });
    }
}


var dynamic_exports = {};


function builder() {
    console.log("in builder");
    console.log(module);
    var names = Object.getOwnPropertyNames(three);
    var n = names.length;
    for (var i = 0; i < 1; i++) {
        var name = names[i];
        var attr = three[name];
        var type = typeof attr;
        if (type === "function") {
            console.log(attr);
            var cls = new ModelTemplate(name);
            dynamic_exports[cls.model_name] = cls;
        }
    }
}


console.log("running builder");
builder();


module.exports = _.extend({}, dynamic_exports, {
    DOMWidgetModel: DOMWidgetModel,
    DOMWidgetView: DOMWidgetView
});
