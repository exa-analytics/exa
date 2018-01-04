// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
import * as ipywidgets from "@jupyter-widgets/base";
var pkgdata = {};


function onmessage(e) {
    console.log("onmessage");
    build(e.mod);
}


function getProtoNames(obj) {
    var names = [];
    for (; obj != null; obj = Object.getPrototypeOf(obj)) {
        var op = Object.getOwnPropertyNames(obj);
        for (var i=0; i<op.length; i++) {
            // If not already added to the list
            if (names.indexOf(op[i]) == -1) {
                names.push(op[i]);
            }
        }
    }
    return names;
}


function buildModelView(viewName, modelName, obj) {

    var attrNames = getProtoNames(obj);

    class Model extends ipywidgets.DOMWidgetModel {
        defaults(): any {
            return {...super.defaults(), ...{
                '_view_name': viewName,
                '_view_module': "exa",
                '_view_module_version': "^0.4.0",
                '_model_name': modelName,
                '_model_module': "exa",
                '_model_module_version': "^0.4.0",
            }};
        }
    }

    class View extends ipywidgets.DOMWidgetView {
        render(): any {
            console.log("Dynamic rendering.");
        }
    }
    
    return {'model': Model, 'view': View, 'attrNames': attrNames};
}


export function build(mod) {
    console.log("In build...");
  //console.log(mod);
    var pydata = {};
    for (var name of Object.getOwnPropertyNames(mod)) {
      //console.log("building: ".concat(name));
        let viewName = name.concat("View");
        let modelName = name.concat("Model");
        var obj = mod[name];
        var mv = buildModelView(viewName, modelName, obj);

        pkgdata[viewName] = mv.view;
        pkgdata[modelName] = mv.model;
        pydata[name] = mv.attrNames;

      //console.log("done with: ".concat(name));
    };

    for (var name of pkgdata) {
        console.log(name);
        export.name = pkgdata[name];
    }
    return pydata;
}
