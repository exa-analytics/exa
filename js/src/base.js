// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Define useful variables and 3rd party modules for which
 * APIs will be generated
 */
"use strict";
var three = require("three");
var three_trackballcontrols = require("three-trackballcontrols");
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

    modules: {
        three: three,
        three_trackballcontrols: three_trackballcontrols
    //    d3: d3
    }
};
