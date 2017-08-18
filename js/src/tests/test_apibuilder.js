// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Tests for APIBuilder
 *
 * Performs a mock creation of the apis.
 */
var ipy = require("jupyter-js-widgets");
var base = require("../base.js");
var three = base.libraries.three;
var trackballcontrols = base.libraries.trackballcontrols;


var DemoModel = ipy.DOMWidgetModel.extend({
    defaults: _.extend({}, ipy.WidgetModel.prototype.defaults, base.defaults, {
        _view_name: "DemoView",
        _model_name: "DemoModel"
    })
});

var DemoView = ipy.DOMWidgetView.extend({
    render: function() {
        var geometry = new three.BoxGeometry(100, 100, 100);
        var material = new three.MeshLambertMaterial({color: "green"});
        var mesh = new three.Mesh(geometry, material);
        var light = new three.AmbientLight(0xFFFFFF, 0.5);
        var dlight = new three.DirectionalLight(0xFFFFFF, 0.3);
        dlight.position.set(100, 100, 100);
        var renderer = new three.WebGLRenderer({antialias: true, alpha: true});
        var camera = new three.PerspectiveCamera(75, 640/480, 0.00001, 100000);
        camera.position.x = 150;
        camera.position.y = 150;
        camera.position.z = 150;
        camera.lookAt(mesh.position);
        var controls = new trackballcontrols(camera, renderer.domElement);
        var scene = new three.Scene();
        scene.fog = new three.FogExp2(0xcccccc, 0.002);
        scene.add(light);
        scene.add(mesh);
        scene.add(camera);
        renderer.setSize(640, 480);
        this.el.appendChild(renderer.domElement);
        console.log(controls);
        renderer.render(scene, camera);
    }
});


module.exports = {
    DemoModel: DemoModel,
    DemoView: DemoView
};
