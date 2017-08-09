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
var imports = require("./imports.js");


/**
 * API Builder Class
 */
class APIBuilderModel extends base.WidgetModel {
    defaults() {
        return _.extend({}, base.WidgetModel.prototype.defaults(), {
            _view_name: "APIBuilderView",
            _model_name: "APIBuilderModel"
        });
    }
}


/**
 * API Builder View
 */
class APIBuilderView extends base.WidgetView {
    /**
     * Called on widget load
     */
    render() {
        console.log("Building API");
        this.build();
    }

    build() {
        console.log(imports);
        var n = imports.length;
        for (var i = 0; i < n; i++) {
            var mod = imports[i];
            console.log(mod);
        }
    }
}


module.exports = {
    APIBuilderModel: APIBuilderModel,
    APIBuilderView: APIBuilderView
}
