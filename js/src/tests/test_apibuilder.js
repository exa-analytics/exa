// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Tests for APIBuilder
 *
 * Performs a mock creation of the apis.
 */
"use strict";
var _ = require("underscore");
var base = require("./base.js");
var modules = require("./imports.js");


class MockAPIBuilderView extends base.WidgetView {
    render() {
        console.log("here");
        this.build();
    }

    build() {
        console.log("building...");
        console.log(modules);
        for (var module in modules) {
            if (modules.hasOwnProperty(module)) {
                console.log(module);
            }
        }
    }
}


class MockAPIBuilderModel extends base.WidgetModel {
    defauts() {
        return _.extend({}, base.WidgetModel.prototype.defaults(), {
            _model_name: "MockAPIBuilderModel",
            _view_name: "MockAPIBuilderView"
        });
    }
}


module.exports = {
    MockAPIBuilderView: MockAPIBuilderView,
    MockAPIBuilderModel: MockAPIBuilderModel
};
