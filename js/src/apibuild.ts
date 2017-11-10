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
var builder = require("./builder.js");
var three = require("three");


export class TestWidgetView extends ipywidgets.DOMWidgetView {
    render(): any {
        console.log("hereererere! ");
        console.log(this.model.get("value"));
        this.el.textContent = this.model.get("value");
        var pkgs = {};

        if (typeof(Worker) === "undefined") {
            console.log("Building API using workers");
            var worker = new Worker("./builder.js");
            worker.postMessage({'mod': three});
        } else {
            console.log("Building API slowly");
            pkgs['three'] = builder.build(three);
        }
        console.log("Created JS API, sending pyapi");
        console.log(pkgs);
        this.send({'method': "build", 'content': pkgs});
    }
}


export class TestWidgetModel extends ipywidgets.DOMWidgetModel {
    defaults(): any {
        return {...super.defaults(), ...{
            '_view_name': "TestWidgetView",
            '_view_module': "jupyter-exa",
            '_view_module_version': "^0.4.0",
            '_model_name': "TestWidgetModel",
            '_model_module': "jupyter-exa",
            '_model_module_version': "^0.4.0",

            'value': "Hello World",
        }};
    }
}
