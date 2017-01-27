// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Exa-ipywidgets Adapter
========================
Interacts with the base ipywidgets (JS) objects (jupyter-js-widgets).
*/
var _ = require("underscore");
var widgets = require("jupyter-js-widgets");
var pythreejs = require("jupyter-threejs");


var HelloWorldView = widgets.DOMWidgetView.extend({
    render: function() {
        this.value_changed();
        this.model.on("change:value", this.value_changed, this);
    },

    value_changed: function() {
        this.el.textContent = this.model.get("value");
    }
});


var HelloWorldModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
        _view_name: "HelloWorldView",
        _model_name: "HelloWorldModel",
        _view_module: "jupyter-exa",
        _model_module: "jupyter-exa",

        value: "Hello World"
    })
});



module.exports = {
    HelloWorldView: HelloWorldView,
    HelloWorldModel: HelloWorldModel
};
