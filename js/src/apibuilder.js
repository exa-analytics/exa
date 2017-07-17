// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Automatic Python API generation for JavaScript libraries.
 * For an example usage see exa-three.js
 * @module
 */
"use strict";
var base = require("./base.js");
var _ = require("underscore");


/**
 * API Builder Class
 */
class APIBuilderModel extends base.DOMWidgetModel {
    get defaults() {
        return _.extend({}, base.DOMWidgetModel.prototype.defaults, {
            _view_name: "APIBuilderView",
            _model_name: "APIBuilderModel"
        });
    }
}


/**
 * API Builder View
 */
class APIBuilderView extends base.DOMWidgetView {
    /**
     * Called on widget load
     */
    render() {
        console.log("here");
    }
}


module.exports = {
    APIBuilderModel: APIBuilderModel,
    APIBuilderView: APIBuilderView
}
