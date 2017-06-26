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
var $ = require("jquery");
//var three = require("three");
//three.TrackballControls = require("three-trackballcontrols");
//console.log(three);


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




var dynamic_exports = {};
var py_classes = {};


function get_args(func) {
    var strfn = func.toString().replace(/((\/\/.*$)|(\/\/*[\s\S]*?\*\/))/mg, "");
    var result = strfn.slice(strfn.indexOf("(") + 1, strfn.indexOf(")")).match(/([^\s,]+)/g);
    if (result === null) {
        result = [];
    }
    return result;
}


function api_builder() {
    var names = Object.getOwnPropertyNames(three);
    var n = names.length;
    for (var i = 0; i < n; i++) {
        var name = names[i];
        var attr = three[name];
        var type = typeof attr;
        if (type === "function") {
            var model_name = name + "Model";
            var argnames = get_args(attr);
            var modelcls = class extends DOMWidgetModel {
                get defaults() {
                    return _.extend({}, DOMWidgetModel.prototype.defaults, {
                        _view_name: view_name,
                        _model_name: model_name,
                        func: attr
                    }, argnames);
                }
            };
            var view_name = name + "View";
            var viewcls = class extends DOMWidgetView {
                render() {
                    var args;
                    var n = argnames.length;
                    for (var i = 0; i < n; i++) {
                        var name = argnames[i];
                        args[name] = this.model.get(name);
                    }
                    this.args = args;
                    this.obj = new this.func(this.args);
                    this.el = this.obj;
                }
            };
            dynamic_exports[model_name] = modelcls;
            dynamic_exports[view_name] = viewcls;
            py_classes[name] = argnames;
        }
    }
}


var classes = {};
var dynamic = {};


/**
 *
 */
class BuilderModel extends DOMWidgetModel {
    /**
     *
     */
    get defaults() {
        return _.extend({}, ipywidgets.DOMWidgetModel.prototype.defaults, {
            _view_name: "BuilderView",
            _view_module: "jupyter-exa",
            _view_module_version: "^0.4.0",
            _model_name: "BuilderModel",
            _model_module: "jupyter-exa",
            _model_module_version: "^0.4.0",

            js_api: null,
            py_api: null
        });
    }
}


/**
 * Dummy view that generates the JavaScript and Python
 * APIs on the fly.
 */
class BuilderView extends DOMWidgetView {
    /**
     * Don't actually render anything, just build the apis
     */
    render() {
        console.log("Building APIs");
        this.extensions = this.model.get("extensions");
        console.log(this.extensions);
        this.dynamic = {};
        this.classes = [];
        this.build();
        this.model.set("dynamic", this.dynamic);
        this.model.set("classes", this.classes);
        dynamic = this.dynamic;
        classes = this.classes;
        this.touch();
    }

    get_args(func) {
        var strfn = func.toString().replace(/((\/\/.*$)|(\/\/*[\s\S]*?\*\/))/mg, "");
        var result = strfn.slice(strfn.indexOf("(") + 1, strfn.indexOf(")")).match(/([^\s,]+)/g);
        if (result === null) {
            result = [];
        }
        return result;
    }

    build() {
        var n = this.extensions.length;
        for (var i = 0; i < n; i++) {
            var name = this.extensions[i];
            var pkg = require(name);
            this.dynamic[name] = pkg;
            this.dynamic[name] = require(name);
            var attributes = Object.getOwnPropertyNames(pkg);
            var nn = attributes.length;
            for (var j = 0; j < nn; j++) {
                var attrname = attributes[j];
                var attr = pkg[attrname];
                var type = typeof attr;
                if (type === "function") {
                    // Build 'model' class definition
                    var model_name = attrname + "Model";
                    var args = this.get_args(attr);
                    var modelcls = class extends DOMWidgetModel {
                        get defaults() {
                            return _.extend({}, DOMWidgetModel.prototype.defaults, {
                                _view_name: view_name,
                                _model_name: model_name,
                                func: attr
                            }, args);
                        }
                    };
                    // Build 'view' class definition
                    var view_name = name + "View";
                    var viewcls = class extends DOMWidgetView {
                        render() {
                            var args;
                            var n = argnames.length;
                            for (var i = 0; i < n; i++) {
                                var name = argnames[i];
                                args[name] = this.model.get(name);
                            }
                            this.args = args;
                            this.obj = new this.func(this.args);
                            this.el = this.obj;
                        }
                    };
                    this.dynamic[model_name] = modelcls;
                    this.dynamic[view_name] = viewcls;
                    this.classes[name] = args;
                }
            }
        }
    }
}


module.exports = _.extend({}, dynamic, {
    DOMWidgetModel: DOMWidgetModel,
    DOMWidgetView: DOMWidgetView,
    BuilderModel: BuilderModel,
    BuilderView: BuilderView
});
