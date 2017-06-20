// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
===========================
Base Widget Model and View
===========================
This module provides the base model and view used by
``exa.core.widget.Widget``.
*/
"use strict";
var ipywidgets = require("jupyter-js-widgets");
var _ = require("underscore");


class WidgetModel extends ipywidgets.WidgetModel {
    get defaults() {
        return _.extend({}, ipywidgets.WidgetModel.prototype.defaults, {
            _view_name: "WidgetView",
            _view_module: "jupyter-exa",
            _view_module_version: "^0.4.0",
            _model_name: "WidgetModel",
            _model_module: "jupyter-exa",
            _model_module_version: "^0.4.0"
        })
    }
}


class WidgetView extends ipywidgets.WidgetView {
    render() {
        console.log("rendered");
    }
}


module.exports = {
    WidgetModel: WidgetModel,
    WidgetView: WidgetView
};
