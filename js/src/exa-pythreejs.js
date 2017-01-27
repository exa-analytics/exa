// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Exa-pythreejs Adapter
=====================
Pythreejs is a Python/JavaScript package that provide a low level interface to
the three.js library. The three.js library can be used to render interactive
applications within the broser using WebGL (among other technologies). This
extension builds a top the pythrejs framework.
*/
var widgets = require("jupyter-js-widgets");
var _ = require("underscore");
//var $ = require("jquery");
var pythreejs = require("jupyter-threejs");


var RendererView = pythreejs.RendererView.extend({
//    render: function() {
//        console.log("inside custom render func");
//        console.log(this);
//        this.camera = new window.THREE.PerspectiveCamera(
//            this.model.get('fov'),
//            this.model.get('aspect'),
//            this.model.get('near'),
//            this.model.get('far')
//        );
//        console.log(this);
//        console.log(typeof this);
//        console.log(Object.prototype.toString.call(this));
//        pythreejs.RendererView.prototype.render.call(this);
//        console.log(this);
//        console.log(typeof this);
//        console.log(Object.prototype.toString.call(this));
//        console.log(typeof this.camera === 'object');
//        console.log(Object.prototype.toString.call(this.scene));
//        console.log(Object.prototype.toString.call(this.camera));
//        console.log(Object.prototype.toString.call(this.camera.obj));
//        console.log(Object.prototype.toString.call(this.camera.prototype));
//    }
});


var RendererModel = pythreejs.RendererModel.extend({
    defaults: _.extend({}, pythreejs.RendererModel.prototype.defaults, {
        _view_name: "RendererView",
        _model_name: "RendererModel",
        _view_module: "jupyter-exa",
        _model_module: "jupyter-exa"
    })
});


console.log(pythreejs.RendererView);
console.log(RendererView);
console.log(pythreejs.RendererView.prototype);
console.log(RendererView.prototype);

console.log(pythreejs.RendererModel);
console.log(RendererModel);
console.log(pythreejs.RendererModel.prototype);
console.log(RendererModel.prototype);

//var SceneView = pythreejs.SceneView; //.extend({});
//
//var SceneModel = pythreejs.SceneModel.extend({
//    defaults: _.extend({}, pythreejs.SceneModel.prototype.defaults, {
//        _view_name: "SceneView",
//        _model_name: "SceneModel",
//        _view_module: "jupyter-exa",
//        _model_module: "jupyter-exa"
//    })
//});


module.exports = {
    RendererView: RendererView,
    RendererModel: RendererModel
//    SceneView: SceneView,
//    SceneModel: SceneModel
};

