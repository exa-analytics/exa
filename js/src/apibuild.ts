// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
import * as jupyterWidgetsBase from "@jupyter-widgets/base";
import * as builder from "./builder";
import * as three from "three";

console.log(jupyterWidgetsBase);



export class TestWidgetView extends jupyterWidgetsBase.WidgetView {
//    render(): any {
//        this.el.textContent = this.model.get("value");
//    }
//        var pkgs = {};
//
//        if (typeof(Worker) === "undefined") {
//            console.log("Building API using workers");
//            var worker = new Worker("./builder.js");
//            worker.postMessage({'mod': THREE});
//        } else {
//            console.log("Building API slowly");
//            pkgs['three'] = builder.build(three);
//        }
//        console.log("Created JS API, sending pyapi");
//        console.log(pkgs);
//        this.send({'method': "build", 'content': pkgs});
//    }
}


export class TestWidgetModel extends jupyterWidgetsBase.WidgetModel {
    initialize(): any {
        console.log("init");
        super.initialize(this, arguments);
        var pkgs = {};
        console.log("Building API synchronously");

        pkgs['three'] = builder.build(three);
        console.log(pkgs);
    }

    defaults(): any {
        return {...super.defaults(), ...{
            '_view_name': "TestWidgetView",
            '_view_module': "exa",
            '_view_module_version': "^0.4.0",
            '_model_name': "TestWidgetModel",
            '_model_module': "exa",
            '_model_module_version': "^0.4.0"
          //'value': "Hello World",
        }};
    }
}
