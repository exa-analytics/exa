// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Automatic Python API generation for JavaScript libraries.
 * For an example usage see exa-three.js
 * @module
 */
"use strict";
var _ = require("underscore");
var base = require("./base.js");
var modules = require("./imports.js");


class APIBuilderView extends base.WidgetView {
    render() {
        console.log("here");
        this.build();
    }

    /**
     * Analyze modules and build an api
     */
    build() {
        console.log("building...");
        console.log(modules);
        for (var module in modules) {
            if (modules.hasOwnProperty(module)) {
                this.analyze_module(module);
            }
        }
    }

    /**
     * Analyze a module, extracting function names and
     * arguments in order to build an API.
     */
    analyze_module(module) {
        console.log("analyzing...", module);
        var names = Object.getOwnPropertyNames(module);
        var n = names.length;
        for (var i = 0; i < n; i++) {
            var name = names[i];
            console.log(name);
        }
    }
}


class APIBuilderModel extends base.WidgetModel {
    defauts() {
        return _.extend({}, base.WidgetModel.prototype.defaults(), {
            _model_name: "APIBuilderModel",
            _view_name: "APIBuilderView"
        });
    }
}


module.exports = {
    APIBuilderView: APIBuilderView,
    APIBuilderModel: APIBuilderModel
};
