// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
========================================
Tests for ``widget.js``
========================================
Test for successful widget creation and bidirectional communication.
*/
"use strict";
var QUnit = require("qunitjs");
var widget = require("jupyter-exa");
var _ = require("underscore");
console.log(QUnit);


class TestWidgetModel extends widget.WidgetModel {
    get defaults() {
        return _.extend({}, widget.WidgetModel.prototype.defaults, {
            _view_name: "TestWidgetView",
            _model_name: "TestWidgetModel",
            text: "Hello World!"
        })
    }
}


class TestWidgetView extends widget.WidgetView {
    render() {
        this.value_changed();
        this.model.on("change:value", this.value_changed, this);
    }

    value_changed() {
        this.el.textContent = this.model.get("value");
    }
}


module.exports = {
    TestWidgetModel: TestWidgetModel,
    TestWidgetView: TestWidgetView
}
