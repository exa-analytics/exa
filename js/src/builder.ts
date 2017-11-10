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
declare function require(name: string);

var ipywidgets = require("@jupyter-widgets/base");
var pkgdata = {};


function onmessage(e) {
    console.log("onmessage");
    build(e.mod);
}


function _proto_helper(obj) {
    if (obj == null) return;
    _proto_helper(Object.getPrototypeOf(obj));
}


function get_proto_names(obj) {
    var names = [];
    for (; obj != null; obj = Object.getPrototypeOf(obj)) {
        var op = Object.getOwnPropertyNames(obj);
        for (var i=0; i<op.length; i++) {
            if (names.indexOf(op[i]) == -1) {
                names.push(op[i]);
            }
        }
    }
    return names;
}


function build_mv(viewname, modelname, obj) {

    var attrnames = get_proto_names(obj);

    class Model extends ipywidgets.DOMWidgetModel {
        defaults(): any {
            return {...super.defaults(), ...{
                '_view_name': viewname,
                '_view_module': "jupyter-exa",
                '_view_module_version': "^0.4.0",
                '_model_name': modelname,
                '_model_module': "jupyter-exa",
                '_model_module_version': "^0.4.0",
            }};
        }
    }

    class View extends ipywidgets.DOMWidgetView {
        render(): any {
            console.log("Dynamic rendering.");
        }
    }
    
    return {'model': Model, 'view': View, 'attrnames': attrnames};
}


export function build(mod) {
    console.log("In build...");
    console.log(mod);
    var pydata = {};
    for (var name of Object.getOwnPropertyNames(mod)) {
        console.log("building: ".concat(name));
        let viewname = name.concat("View");
        let modelname = name.concat("Model");
        var obj = mod[name];
        var mv = build_mv(viewname, modelname, obj);

        pkgdata[viewname] = mv.view;
        pkgdata[modelname] = mv.model;
        pydata[name] = mv.attrnames;

        console.log("done with: ".concat(name));
    };
    return pydata;

}


for (var name of pkgdata) {
    export.name = pkgdata[name];
}
