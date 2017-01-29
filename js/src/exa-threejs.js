// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Exa-three.js Adapter
=====================
*/
"use strict";
var widgets = require("jupyter-js-widgets");
var THREE = require("three");


class RendererView extends widgets.DOMWidgetView {
    render() {
        this.camera = new THREE.PerspectiveCamera(75, 600/450, 1, 1000);
        this.camera.position.z = 500;
        this.scene = new THREE.Scene();
        this.geom = new THREE.IcosahedronGeometry(200, 1);
        this.mat = new THREE.MeshBasicMaterial({
            color: "red",
            wireframe: true,
            wireframelinewidth: 8
        });
        this.mesh = new THREE.Mesh(this.geom, this.mat);
        this.scene.add(this.mesh);
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });
        this.renderer.setSize(600, 400);
        this.el.appendChild(this.renderer.domElement);
        this.renderer.render(this.scene, this.camera);
        this.animation();
    };
    
    animation() {
        window.requestAnimationFrame(this.animation.bind(this));
        this.mesh.rotation.x = Date.now()*0.00005;
        this.mesh.rotation.y = Date.now()*0.0001;
        this.mesh.position.y += 0.0005;
        this.mesh.position.z += 0.05;
        this.renderer.render(this.scene, this.camera);
    };
}


class RendererModel extends widgets.DOMWidgetModel {
    get defaults() {
        return _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
            _view_name: "RendererView",
            _view_module: "jupyter-exa",
            _model_name: "RendererModel",
            _model_module: "jupyter-exa"
        });
    }
}


module.exports = {
    "RendererView": RendererView,
    "RendererModel": RendererModel
};

