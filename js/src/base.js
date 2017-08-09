// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * This module provides the base model and view used by
 * exa.core.widget.DOMWidget.
 * @module
 */
"use strict";
var ipyw = require("jupyter-js-widgets");
//var ipyw = require("@jupyter-widgets/base");    // ipywidgets >= 7.0.0
var _ = require("underscore");
var jsver = "^0.4.0";
var jsmod = "jupyter-exa";


/**
 * Base Model Class
 *
 * The Widget can be used to create "hidden" JavaScript functionality.
 * For interactive (visual) widgets use DOMWidget instead.
 */
class WidgetModel extends ipyw.WidgetModel {
    defaults() {
        return _.extend({}, ipyw.WidgetModel.prototype.defaults, {
            _view_name: "WidgetView",
            _view_module: jsmod,
            _view_module_version: jsver,
            _model_name: "WidgetModel",
            _model_module: jsmod,
            _model_module_version: jsver
        });
    }
}


/**
 * Base View Class
 */
class WidgetView extends ipyw.WidgetView {
    render() {
        console.log("widgetview");
    }
}


/**
 * Base (DOM) Model Class
 */
class DOMWidgetModel extends ipyw.DOMWidgetModel {
    /**
     * Used by Jupyter
     */
    defaults() {
        return _.extend({}, ipyw.DOMWidgetModel.prototype.defaults, {
            _view_name: "DOMWidgetView",
            _view_module: jsmod,
            _view_module_version: jsver,
            _model_name: "DOMWidgetModel",
            _model_module: jsmod,
            _model_module_version: jsver
        });
    }
}


/**
 * Base (DOM) View Class
 */
class DOMWidgetView extends ipyw.DOMWidgetView {
}


module.exports = {
    jsver: jsver,
    jsmod: jsmod,
    WidgetModel: WidgetModel,
    WidgetView: WidgetView,
    DOMWidgetModel: DOMWidgetModel,
    DOMWidgetView: DOMWidgetView
}
