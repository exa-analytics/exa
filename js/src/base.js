// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Base Definitions
 *
 * This module defines useful variables and sets what 3rd party JavaScript
 * libraries will have dynamically generated APIs. Note that throughout
 * the JavaScript code we do not use ES6 classes. Although conceptually
 * convient they do not work well with Backbone.js. Backbone.js is used by
 * the ipywidgets framework ('widgetsnbextension') in order to create
 * bi-directional communication between the notebook's JavaScript frontend
 * and the IPython kernel's Python backend.
 */
"use strict";
var three = require("three");
var trackballcontrols = require("three-trackballcontrols");
//var d3 = require("d3");

var module_version = "^0.4.0";
var module_name = "jupyter-exa";


module.exports = {
    defaults: {
        _model_module: module_name,
        _model_module_version: module_version,
        _view_module: module_name,
        _view_module_version: module_version
    },

    libraries: {
        three: {lib: three, ignore: ["VideoTexture"]},
        trackballcontrols: {lib: trackballcontrols, ignore: []}
    //    d3: d3
    }
};
