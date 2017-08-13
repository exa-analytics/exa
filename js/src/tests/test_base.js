// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Generic Widget Tests
 */
"use strict";
var _ = require("underscore");
//var ipy = require("@jupyter-widgets/base");    // >=7.x
var ipy = require("jupyter-js-widgets");    // <=6.x
var base = require("../base.js");


var DOMWidgetTestModel = ipy.DOMWidgetModel.extend({
    defaults: _.extend({}, ipy.DOMWidgetModel.prototype.defaults, base.defaults, {
        _model_name: "DOMWidgetTestModel",
        _view_name: "DOMWidgetTestView",
        value: "Hello World"
    })
});


var DOMWidgetTestView = ipy.DOMWidgetView.extend({
    render: function() {
        this.value_changed();
        this.model.on("change:value", this.value_changed, this);
    },

    value_changed: function() {
        console.log(this);
        console.log(this.el);
        this.el.textContent = this.model.get("value");
    }
});


/**
 * Test non DOM widgets
 */
var WidgetTestModel = ipy.WidgetModel.extend({
    defaults: _.extend({}, ipy.WidgetModel.prototype.defaults, base.defaults, {
        _model_name: "WidgetTestModel",
        _view_name: "WidgetTestView"
    })
});


/**
 * Test non DOM Widgets
 */
var WidgetTestView = ipy.WidgetView.extend({
    render: function() {
        this.log_value();
        this.send_value();
    },

    log_value: function() {
        var value = this.model.get("value");
        console.log(value);
    },

    send_value: function() {
        var value = this.model.get("value");
        this.send(value);
    }
});


module.exports = {
    WidgetTestModel: WidgetTestModel,
    WidgetTestView: WidgetTestView,
    DOMWidgetTestModel: DOMWidgetTestModel,
    DOMWidgetTestView: DOMWidgetTestView
};
