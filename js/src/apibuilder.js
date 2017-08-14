// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Automatic Python API generation for JavaScript libraries.
 * For an example usage see exa-three.js
 * @module
 */
"use strict";
var _ = require("underscore");
//var ipy = require("@jupyter-widgets/base");    // >=7.x
var ipy = require("jupyter-js-widgets");    // <=6.x
var base = require("./base.js");
// These variables store dynamically created models and views (for backbone.js)
var exports = {};
var pyclasses = {};


var APIBuilderView = ipy.WidgetView.extend({
    render: function() {
        console.log("Sending architecture for building Python classes.");
        this.send({'method': "build", 'content': pyclasses});
    }
});


var APIBuilderModel = ipy.WidgetModel.extend({
    defauts: _.extend({}, ipy.WidgetModel.prototype.defaults, base.defaults, {
        _model_name: "APIBuilderModel",
        _view_name: "APIBuilderView"
    })
});


/**
 * Identify string argument names of a function/class.
 */
function get_arg_names(func) {
    var strfn = func.toString().replace(/((\/\/.*$)|(\/\/*[\s\S]*?\*\/))/mg, "");
    var result = strfn.slice(strfn.indexOf("(") + 1, strfn.indexOf(")")).match(/([^\s,]+)/g);
    if (result === null) {
        result = [];
    }
    return result;
}


/**
 * Create the model and view
 *
 * By separating the class creation into a function, we force a 'new' instance
 * of the (backbon.js) prototype to be made.
 */
function create_mv(name, attr, argnames) {
    var vname = name + "View";
    var mname = name + "Model";

    var modelcls = ipy.DOMWidgetModel.extend({
        defaults: _.extend({}, ipy.DOMWidgetModel.prototype.defaults, base.defaults, {
            _view_name: vname,
            _model_name: mname
        })
    });

    var viewcls = ipy.DOMWidgetView.extend({
        render: function() {
            console.log("Hello from...", name);
            console.log(attr);
            var args = {};
            var n = argnames.length;
            for (var i = 0; i < n; i++) {
                var argname = argnames[i];
                args[argname] = this.model.get(argname);
            }
            console.log(args);
            this.obj = new attr(args);
            console.log(this.obj);
            this.el.appendChild(this.obj.domElement);
        }
    });

    return {
        view: viewcls,
        model: modelcls
    };
};


/**
 * Analyze a module, extracting function names and
 * arguments in order to build an API.
 */
function analyze_module(modname, module) {
    console.log("Analyzing module...", module);
    pyclasses[modname] = {};
    var names = Object.getOwnPropertyNames(module);
    var n = names.length;
    for (var i = 0; i < n; i++) {
        var name = names[i];
        var attr = module[name];
        var type = typeof attr;
        if (type === "function") {
            var view_name = name + "View";
            var model_name = name + "Model";
            var argnames = get_arg_names(attr);
            var classes = create_mv(name, attr, argnames);
            exports[view_name] = classes.view;
            exports[model_name] = classes.model;
            pyclasses[modname][name] = argnames;
        };
    };
};


/**
 * Analyze modules and build an api
 */
function build() {
    console.log("Building Models and Views...");
    for (var modname in base.modules) {
        if (base.modules.hasOwnProperty(modname)) {
            analyze_module(modname, base.modules[modname]);
        }
    }
}


// Call the builder so that we can export the required models and views
build();
exports['APIBuilderView'] = APIBuilderView;
exports['APIBuilderModel'] = APIBuilderModel;


//var AmbientLightModel = ipy.DOMWidgetModel.extend({
//    defaults: _.extend({}, ipy.DOMWidgetModel.prototype.defaults, base.defaults, {
//        _model_name: "AmbientLightModel",
//        _view_name: "AmbientLightView",
//        value: "Hello World...."
//    })
//});
//
//
//var AmbientLightView = ipy.DOMWidgetView.extend({
//    render: function() {
//        this.value_changed();
//        this.model.on("change:value", this.value_changed, this);
//    },
//
//    value_changed: function() {
//        console.log(this);
//        console.log(this.el);
//        this.el.textContent = this.model.get("value");
//    }
//});
//
//exports['AmbientLightView'] = AmbientLightView;
//exports['AmbientLightModel'] = AmbientLightModel;
//pyclasses['three'] = {};
//pyclasses['three']['WebGLRenderer'] = ["value"];
console.log(exports);
console.log(exports['AmbientLightView']);
console.log(exports['AmbientLightModel']);


module.exports = exports;
