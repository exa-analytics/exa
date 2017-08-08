// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Tests for Base Widgets
 *
 * The code here tests functionality in ``base.js``. Tests are executed
 * by Python and are contained within the Jupyter framework; they are not
 * standalone JavaScript unittests.
 */
"use strict";
var _ = require("underscore");
var base = require("../base.js");


class DOMWidgetTestModel extends base.DOMWidgetModel {
    defaults() {
        return _.extend({}, base.DOMWidgetModel.prototype.defaults, {
            _model_name: "DOMWidgetTestModel",
            _view_name: "DOMWidgetTestView",
            value: "Hello World"
        });
    }
}


class DOMWidgetTestView extends base.DOMWidgetView {
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


/**
 * Test non DOM widgets
 */
class WidgetTestModel extends base.WidgetModel {
    defaults() {
        return _.extend({}, base.WidgetModel.prototype.defaults, {
            _model_name: "WidgetTestModel",
            _view_name: "WidgetTestView"
        });
    }
}


/**
 * Test non DOM Widgets
 */
class WidgetTestView extends base.WidgetView {
    render() {
        this.log_value();
        this.send_value();
    }

    log_value() {
        var value = this.model.get("value");
        console.log(value);
    }

    send_value() {
        var value = this.model.get("value");
        this.send(value);
    }
}



module.exports = {
    WidgetTestModel: WidgetTestModel,
    WidgetTestView: WidgetTestView,
    DOMWidgetTestModel: DOMWidgetTestModel,
    DOMWidgetTestView: DOMWidgetTestView
};
