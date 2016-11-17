// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Exa-Three.js Adapter
=====================
Description
*/
var widgets = require("jupyter-js-widgets");
var _ = require("underscore");
var THREE = require("three");
window.THREE = THREE;    // Allows importing three/*
require("./threejs/renderers/CanvasRenderer.js");
var Detector = require("./threejs/Detector.js");


function build_api() {
    var models = {};
    var views = {};
    var len = THREE.length;
    for (var i = 0; i < len; i++) {
        console.log(THREE[i]);
    }
    return _.extend({}, models, views);
}

module.exports = build_api();
