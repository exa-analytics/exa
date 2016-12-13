// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Exa-Three.js Adapter
=====================
Description
*/
var widgets = require("jupyter-js-widgets");
var _ = require("underscore");
var $ = require("jquery");
var pythreejs = require("jupyter-threejs");
var THREE = require("three");
window.THREE = THREE;    // Allows importing three/*
var base = require("./foo/base.js");


// The DOM object is what is actually displayed in the (Jupyter) notebook
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


// All other objects are just Widgets
class ThreeView extends widgets.WidgetView {
}

class ThreeModel extends widgets.WidgetModel {
}


//


function generate_view(name) {
    console.log("generate_view");
//    console.log(THREE[name]);
//    console.log(THREE[name].prototype);
 //   var obj = THREE[name];
 //   console.log(obj);

    return {};
}


function build_api() {
    console.log("building api");
    var models = {RendererModel: RendererModel};
    var views = {RendererView: RendererView};
    console.log(THREE);
    for (var attribute in THREE) {
        if (THREE.hasOwnProperty(attribute)) {
            console.log(attribute);
        }
    }
    console.log("EDIT");
    console.log(pythreejs);
//    var obj = THREE.BoxGeometry();
//    console.log(obj);
    //var attributes = generate_view("BoxGeometry");

    return _.extend({}, models, views);
}

module.exports = build_api();
