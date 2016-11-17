// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Widget
=================
Description
*/
'use strict';
var widgets = require("jupyter-js-widgets");
var _ = require("underscore");


function createWidgetModel(name, defaults) {
    /*"""
    createWidgetModel
    ===================
    Generates a model for the widget.
    */
    var model_name = name + "Model";
    var view_name = name + "View";
    var ipywidgets_params = {"_model_name": model_name, "_view_name": view_name,
                             "_model_module": "jupyter-exa",
                             "_view_module": "jupyter-exa"};
    return widgets.DOMWidgetModel.extend({
        defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults,
                           ipywidgets_params, defaults)
    });
}


module.exports = {
    createWidgetModel: createWidgetModel
};
