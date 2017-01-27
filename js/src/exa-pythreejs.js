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
//var widgets = require("jupyter-js-widgets");
//var $ = require("jquery");
var _ = require("underscore");
var pythreejs = require("jupyter-threejs");


//var RendererView = pythreejs.RendererView.extend({
//    constructor: function() {
//        pythreejs.RendererView.apply(this, arguments);
//    }
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
//});



//var RendererModel = pythreejs.RendererModel.extend({
//    defaults: _.extend({}, pythreejs.RendererModel.prototype.defaults, {
//        _view_name: "RendererView",
//        _model_name: "RendererModel",
//        _view_module: "jupyter-exa",
//        _model_module: "jupyter-exa"
//    })
//});

//var ExaRendererView = pythreejs.RendererView.extend({
//    render: function() {
//        console.log("in custom view render func");
//        pythreejs.RendererView.prototype.render.call(this);
//        console.log(this);
//        console.log(typeof this);
//        console.log(Object.prototype.toString.call(this));
//    }
//});
//var ExaRendererModel = pythreejs.RendererModel;
//RendererModel.prototype.defaults['_view_name'] = 

//console.log(pythreejs.RendererView);
//console.log(ExaRendererView);
//console.log(pythreejs.RendererView.prototype);
//console.log(ExaRendererView.prototype);
//
//console.log(pythreejs.RendererModel);
//console.log(ExaRendererModel);
//console.log(pythreejs.RendererModel.prototype);
//console.log(ExaRendererModel.prototype);

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


var ExaRendererModel = pythreejs.RendererModel.extend({
    defaults: _.extend({}, pythreejs.RendererModel.prototype.defaults, {
        _view_name: "RendererView",
        _model_name: "ExaRendererModel",
        _view_module: "jupyter-three",
        _model_module: "jupyter-exa"
    })
});


module.exports = {
    ExaRendererModel: ExaRendererModel
//    ExaRendererView: ExaRendererView
//    ExaRendererModel: ExaRendererModel
//    SceneView: SceneView,
//    SceneModel: SceneModel
};

