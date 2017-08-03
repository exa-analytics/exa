// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Tests for Base Widgets
 */
"use strict";
//var QUnit = require("qunitjs");
var _ = require("underscore");
var base = require("../base.js");



class HelloModel extends base.DOMWidgetModel {
    defaults() {
        return _.extend({}, base.DOMWidgetModel.prototype.defaults(), {
            _model_name: "HelloModel",
            _model_module: base.jsmod,
            _model_version: base.jsver,
            _view_name: "HelloView",
            _view_module: base.jsmod,
            _view_version: base.jsver,
            value: "Hello World"
        });
    }
}


class HelloView extends base.DOMWidgetView {
    render() {
        this.value_changed();
        this.model.on("change:value", this.value_changed, this);
    }

    value_changed() {
        console.log(this);
        console.log(this.el);
        this.el.textContent = this.model.get("value");
    }
}


module.exports = {
    HelloModel: HelloModel,
    HelloView: HelloView
};
