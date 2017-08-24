// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Automatic Python API generation for JavaScript libraries.
 *
 * This module scans predefined third party JavaScript libraries (e.g. three.js)
 * and identifies top level objects for which an API is dynamically generated.
 * This API allows developers and users to access features of third-party
 * libraries directly from Python (through the ipywidgets - itself built on
 * Backbone.js - infrastructure). An attempt is made to provide a fully featured
 * API automatically but this may not always be possible.
 *
 * See the style comment in base.js for technical information about syntax and
 * style.
 */
"use strict";
var _ = require("underscore");
//var ipy = require("@jupyter-widgets/base");    // >=7.x
var ipy = require("jupyter-js-widgets");    // <=6.x
var base = require("./base.js");
// These variables store dynamically created models and views (for backbone.js)
// The exports variable contains (Backbone.js via ipywidgets' widgetsnbextension
// module) Model and View objects.
var jsexports = {};
// The pyexports contains a full specification of a single ipywidgets 'Widget'
// to be created (dynamically) in Python.
var pyexports = {};



/**
 * Python API Builder Widget View
 *
 * This widget is responsible for sending dynamically generated
 * class skeletons to Python for API creation.
 */
var APIBuilderView = ipy.WidgetView.extend({
    render: function() {
        // 'Rendering' this widget simply sends classes skeletons to
        // the Python backend for Python API creation.
        console.log("Sending class skeletons for Python API creation...");
        this.send({'method': "build", 'content': pyexports});
    },

    on_msg: function(args) {
        console.log("MESSAGE RECIEVED....", args);
    }
});


/**
 * Python API Builder Widget Model
 */
var APIBuilderModel = ipy.WidgetModel.extend({
    defauts: _.extend({}, ipy.WidgetModel.prototype.defaults, base.defaults, {
        _model_name: "APIBuilderModel",
        _view_name: "APIBuilderView"
    })
});


/**
 * Analyze a function (or class) and determine arguments (class constructor
 * arguments) and method names. Return a dictionary of these values names
 * as strings. Used to create a skeleton for Python API creation.
 */
function analyze_object(obj) {
    var strobj = obj.toString().replace(/((\/\/.*$)|(\/\/*[\s\S]*?\*\/))/mg, "");
    var args = strobj.slice(strobj.indexOf("(")+1, strobj.indexOf(")")).match(/([^\s,]+)/g);
    if (args === null) {
        args = [];
    }

    var methods = Object.getOwnPropertyNames(new obj());

//    try {
//        methods = Object.getOwnPropertyNames(new obj());
//    }
//    finally {}

    return {
        args: args,
        methods: methods
    };
}


/**
 * Model and View Creation
 *
 * This function creates two 'class' definitions and (Backbone.js) Model  and
 * View. By separating creation into a separate function we avoid multiple
 * referencing of variables (used in class definition creation).
 */
function create_mv(name, obj) {
    //var vname = name + "View";
    //var mname = name + "Model";

    var modelcls = ipy.DOMWidgetModel.extend({
        defaults: _.extend({}, ipy.DOMWidgetModel.prototype.defaults, base.defaults, {
            _view_name: name + "View",
            _model_name: name + "Model"
        })
    });

    var viewcls = ipy.DOMWidgetView.extend({
        render: function() {
            console.log("Rendering...", name);
            console.log(obj);
//            var args = {};
//            var n = argnames.length;
//            for (var i = 0; i < n; i++) {
//                var argname = argnames[i];
//                args[argname] = this.model.get(argname);
//            }
//            console.log(args);
//            this.obj = new attr(args);
//            console.log(this.obj);
//            console.log(document.getElementById(this));
//            console.log(document.getElementById(this.obj));
//            // TODO THIS DOESNT WORK FOR EVERYTHING
//            this.el.appendChild(this.obj.domElement);
        }
    });

    return {
        view: viewcls,
        model: modelcls
    };
};


/**
 * Analyze JavaScript Library
 *
 * This function analyzes a JavaScript library, identifies top level API
 * functions/classes and populates the `jsexports' and `pyexports' global
 * variables used to create a dynamic API. The API exists in the Python
 * backend and can be used after importing the Python package. It utilizes
 * the infrastructure provided by ipywidgets for bidirectional communication
 * between JavaScript and Python. The use case is for dynamic frontend
 * content powered by JavaScript in the Jupyter notebook, with the data
 * coming from a Python data processing backend.
 */
function analyze_library(libname, library, ignore) {
    console.log("Analyzing the ", libname, " library/function/class");
    // If the library is actually just a function things are easier to
    // handle so we check for that first.
    if (typeof library === "function") {
        console.log("LIB IS FUNC");
        console.log(libname);
    }
    pyexports[libname] = {};
    var topnames = Object.getOwnPropertyNames(library);
    var n = topnames.length;
    for (var i = 0; i < n; i++) {
        var topname = topnames[i];
        var topobj = library[topname];
        var prototype = Object.getPrototypeOf(topobj);
//        if (prototype.hasOwnProperty("constructor")) {
//            var skeleton = analyze_object(topobj);
//            var mvclasses = create_mv(topname, topobj);
//            jsexports[topname+"View"] = mvclasses.view;
//            jsexports[topname+"Model"] = mvclasses.model;
//            pyexports[topname] = skeleton;
//        }
    }
}


/**
 * Build the API
 *
 * This function iterates over imported libraries predefined for API
 * creation.
 */
function build() {
    console.log("Starting API construction...");
    for (var libname in base.libraries) {
        if (base.libraries.hasOwnProperty(libname)) {
            var library = base.libraries[libname].lib;
            var ignore = base.libraries[libname].ignore;
            analyze_library(libname, library, ignore);
        }
    }
}


// The build function iterates over the imported libraries
// and populates the global variables `jsexports` and `pyexports`.
build();
// Add additional exports.
jsexports['build'] = build;
jsexports['analyze_library'] = analyze_library;
jsexports['analyze_object'] = analyze_object;
jsexports['create_mv'] = create_mv;
jsexports['APIBuilderView'] = APIBuilderView;
jsexports['APIBuilderModel'] = APIBuilderModel;


console.log("SUMMARY");
console.log(jsexports);
console.log(pyexports);
console.log(APIBuilderView);
console.log(APIBuilderModel);

console.log(base.libraries.three);


module.exports = jsexports;
