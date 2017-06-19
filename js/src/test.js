// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
=============
test.js
=============
A test application called when an empty container widget is rendered in a
Jupyter notebook environment.
*/
"use strict";
var THREE = require("three");
var base = require("./base.js");
var bthree = require("./base-three.js");
var App3D = require("./app3d.js").App3D;
var Field = require("./field.js").ScalarField;
var num = require("./num.js");


class TestSceneModel extends bthree.ThreeSceneModel {

    get defaults() {
        return _.extend({}, bthree.ThreeSceneModel.prototype.defaults, {
            _model_name: "TestModel",
            _view_name: "TestView",
            geo_shape: false,
            geo_color: false,
            field_iso: 2.0,
            field: "null",
            field_nx: 20,
            field_ny: 20,
            field_nz: 20,
        })
    }

}


class TestSceneView extends bthree.ThreeSceneView {

    init() {
        super.init();
        this.init_listeners();
        this.test_geometry();
        this.field_params = {
            "isoval": this.model.get("field_iso"),
            "boxsize": 3.0,
            "nx": this.model.get("field_nx"),
            "ny": this.model.get("field_ny"),
            "nz": this.model.get("field_nz"),
            "ox": -3.0, "oy": -3.0, "oz": -3.0,
            "fx":  3.0, "fy":  3.0, "fz":  3.0,
            "dxi": 0.5, "dyj": 0.5, "dzk": 0.5,
            "dxj": 0.0, "dyi": 0.0, "dzi": 0.0,
            "dxk": 0.0, "dyk": 0.0, "dzj": 0.0,
        };
        this.app3d = new App3D(this);
        this.add_meshes();
        this.animation();
    }

    /*
    render() {
        this.renderer.render(this.scene, this.camera);
    }
    */

    test_geometry(color) {
        color = (typeof color === "undefined") ? "red" : color;
        var geom = new THREE.IcosahedronGeometry(2, 1);
        var mat = new THREE.MeshBasicMaterial({
            color: color,
            wireframe: true
        });
        var mesh = new THREE.Mesh(geom, mat);
        this.meshes.push(mesh);
    }

    shape_scene() {
        this.clear_meshes();
        this.test_geometry();
        this.add_meshes();
    }

    color_scene() {
        var color = (this.model.get("geo_color") === true) ? "black": "red";
        this.clear_meshes();
        this.test_geometry(color);
        this.add_meshes();
    }

    field_scene() {
        this.clear_meshes();
        var field_type = this.model.get("field");
        this.field_params["isoval"] = this.model.get("field_iso");
        this.field_params["nx"] = this.model.get("field_nx");
        this.field_params["ny"] = this.model.get("field_ny");
        this.field_params["nz"] = this.model.get("field_nz");
        var thisfield = new Field(this.field_params,
                                              num[field_type]);
        this.meshes = this.app3d.add_scalar_field(thisfield,
                                                  this.field_params.isoval);
        this.add_meshes();
    }

    init_listeners() {
        this.listenTo(this.model, "change:geo_shape", this.shape_scene);
        this.listenTo(this.model, "change:geo_color", this.color_scene);
        this.listenTo(this.model, "change:field", this.field_scene);
        this.listenTo(this.model, "change:field_nx", this.field_scene);
        this.listenTo(this.model, "change:field_ny", this.field_scene);
        this.listenTo(this.model, "change:field_nz", this.field_scene);
        this.listenTo(this.model, "change:field_iso", this.field_scene);
    }

}


class TestContainerModel extends base.BaseBoxModel {
    get defaults() {
        return _.extend({}, base.BaseBoxModel.prototype.defaults, {
            _model_name: "TestContainerModel",
            _view_name: "TestContainerView"
        })
    }
}


class TestContainerView extends base.BaseBoxView {
    render() {
        console.log("test container view render");
        super.render();
    }
}

<<<<<<< HEAD
=======
    render_field() {
        this.app3d.remove_meshes(this.meshes);
        this.meshes = this.app3d.add_scalar_field(this.fields.field, this.fields.isovalue, this.fields.sides);
        this.app3d.set_camera({"x": 7.5, "y": 7.5, "z": 7.5});
    };
};
>>>>>>> tjduignamaster

module.exports = {
    TestSceneModel: TestSceneModel,
    TestSceneView: TestSceneView,
    TestContainerModel: TestContainerModel,
    TestContainerView: TestContainerView
}
