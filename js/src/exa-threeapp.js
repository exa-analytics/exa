// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Subclassing example
===================
*/
"use strict";
var THREE = require("three");
var exathreejs = require("./exa-threejs.js");


class SubRendererView extends exathreejs.RendererView {
    render() {
        this.camera = new THREE.PerspectiveCamera(75, 600/450, 1, 1000);
        this.camera.position.z = 500;
        this.scene = new THREE.Scene();
        this.geom = new THREE.IcosahedronGeometry(200, 1);
        this.mat = new THREE.MeshBasicMaterial({
            color: "purple",
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


class SubRendererModel extends exathreejs.RendererModel {
    get defaults() {
        return _.extend({}, exathreejs.RendererModel.prototype.defaults, {
            _view_name: "SubRendererView",
            _view_module: "jupyter-exa",
            _model_name: "SubRendererModel",
            _model_module: "jupyter-exa"
        });
    }
}


module.exports = {
    "SubRendererView": SubRendererView,
    "SubRendererModel": SubRendererModel
};

