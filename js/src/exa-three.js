// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Exa-Three.js Adapter
=====================
Description
*/
var widgets = require("jupyter-js-widgets");
var _ = require("underscore");
var base = require("./foo/base.js");
var THREE = require("three");
window.THREE = THREE;    // Allows importing three/*
require("./threejs/renderers/CanvasRenderer.js");
var Detector = require("./threejs/Detector.js");


// Core three.js objects
var RendererModel = base.createWidgetModel("Renderer", {"value": "renderer model"});

class RendererView extends widgets.DOMWidgetView {
    render() {
        this.value_changed();
        this.model.on("change:value", this.value_changed, this);
    }

    value_changed() {
        this.el.textContent = this.model.get("value");
    }
}

function build_api() {
    console.log("building api");
    var models = {RendererModel: RendererModel};
    var views = {RendererView: RendererView};
    var len = THREE.length;
    console.log(len);
    for (var i = 0; i < len; i++) {
        console.log(THREE[i]);
    }

    return _.extend({}, models, views);
}

module.exports = build_api();
