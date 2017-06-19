// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
=================
base-three.js
=================
*/
var base = require("./base.js");
var THREE = require("three");
var TBC = require("three-trackballcontrols");

class ThreeSceneModel extends base.BaseDOMModel {

    get defaults() {
        return _.extend({}, base.BaseDOMModel.prototype.defaults, {
            _model_name: "ThreeSceneModel",
            _view_name: "ThreeSceneView",
            scn_clear: false,
            scn_saves: false,
            savedir: "",
            imgname: ""
        })
    }

    aspectRatio() {
        return this.get("layout").get("width") / this.get("layout").get("height");
    }

}

class ThreeSceneView extends base.BaseDOMView {

    init() {
        this.meshes = [];

        this.camera = new THREE.PerspectiveCamera(35, this.model.aspectRatio(), 1, 1000);
        this.camera.position.z = 10;

        this.scene = new THREE.Scene();
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });
        this.renderer.setSize(this.model.get("layout").get("width"),
                              this.model.get("layout").get("height"));
        this.el.appendChild(this.renderer.domElement);

        this.controls = new TBC(this.camera, this.renderer.domElement);
        this.controls.rotateSpeed = 10.0;
        this.controls.zoomSpeed = 5.0;
        this.controls.panSpeed = 0.5;
        this.controls.noZoom = false;
        this.controls.noPan = false;
        this.controls.staticMoving = true;
        this.controls.dynamicDampingFactor = 0.3;
        this.controls.keys = [65, 83, 68];
        this.controls.addEventListener("change", this.render.bind(this));
        this.controls.target = new THREE.Vector3(0.0, 0.0, 0.0);

        this.base_listeners();
        this.render();
        this.animation();
    }

    render() {
        this.renderer.render(this.scene, this.camera);
    }

    resize(w, h) {
        this.model.get("layout").set("width", w);
        this.model.get("layout").set("height", h);
        this.renderer.setSize(w, h);
        this.camera.aspect = this.model.aspectRatio();
        this.camera.updateProjectionMatrix();
        this.controls.handleResize();
        this.render();
    }

    animation() {
        window.requestAnimationFrame(this.animation.bind(this));
        this.render();
        this.controls.update();
        this.resize(this.model.get("layout").get("width"),
                    this.model.get("layout").get("height"));
    }

    clear_meshes() {
        for (var idx in this.meshes) {
            this.scene.remove(this.meshes[idx]);
        };
        this.meshes = [];
        this.render();
    }

    add_meshes() {
        for (var idx in this.meshes) {
            this.scene.add(this.meshes[idx]);
        };
        this.render();
    }

    scene_save() {
        this.renderer.setSize(1920, 1080);
        this.camera.aspect = 1920 / 1080;
        this.camera.updateProjectionMatrix();
        this.render();
        var image = this.renderer.domElement.toDataURL("image/png");
        this.send({"type": "image", "content": image});
        this.renderer.setSize(this.model.get("layout").get("width"),
                              this.model.get("layout").get("height"));
        this.camera.aspect = this.model.aspectRatio();
        this.camera.updateProjectionMatrix();
        this.render();
    }

    base_listeners() {
        this.listenTo(this.model, "change:scn_clear", this.clear_meshes);
        this.listenTo(this.model, "change:scn_saves", this.scene_save);
    }

}

module.exports = {
    ThreeSceneModel: ThreeSceneModel,
    ThreeSceneView: ThreeSceneView
}
