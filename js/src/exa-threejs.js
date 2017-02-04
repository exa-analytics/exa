// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Exa-three.js Adapter
=====================
*/
"use strict";
var widgets = require("jupyter-js-widgets");
var THREE = require("three");
//var $ = require("jquery");


class RendererView extends widgets.DOMWidgetView {
    render() {
        var button = document.createElement("button");
        button.value = "button";
        button.text = "other";
        button.classList.add("button");
        console.log(button);
        var css = document.createElement("style");
        css.innerHTML = ".button {\
            background-color: #4CAF50; /* Green */\
            border: none;\
            color: black;\
            padding: 15px 32px;\
            text-align: center;\
            text-decoration: none;\
            display: inline-block;\
            font-size: 20px;\
            height: 100px;\
            width: 300px;\
            position: absolute;\
            left: 0px;\
            top: 0px;\
            opacity: 0.5;\
        }";
        console.log(css);
//        button.style = css;
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
        var self = this;
        var el = $("<div/>").width(700).height(400).resizable({
            aspectRatio: false,
            resize: function(event, ui) {
                self.el.width = ui.size.width;
                self.el.height = ui.size.height;
                self.renderer.setSize(self.el.width, self.el.height);
                self.camera.aspect = self.el.width/self.el.height;
                self.camera.updateProjectionMatrix();
            },
        });
        el.append(this.renderer.domElement);
        el.append(button);
        el.append(css);
        console.log(el);
        this.setElement(el);
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

