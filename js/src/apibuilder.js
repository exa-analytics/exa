// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Automatic Python API generation for JavaScript libraries.
 * For an example usage see exa-three.js
 * @module
 */
"use strict";
var _ = require("underscore");
var base = require("./base.js");
var modules = require("./imports.js");


class APIBuilderView extends base.WidgetView {
    render() {
        console.log("here");
        this.exports = {};
        this.build();
        console.log(this.exports);
    }

    /**
     * Analyze modules and build an api
     */
    build() {
        console.log("building...");
        console.log(modules);
        for (var modname in modules) {
            if (modules.hasOwnProperty(modname)) {
                this.analyze_module(modname, modules[modname]);
            }
        }
    }

    /**
     * Analyze a module, extracting function names and
     * arguments in order to build an API.
     */
    analyze_module(modname, module) {
        console.log("analyzing...", module);
        var names = Object.getOwnPropertyNames(module);
        var n = names.length;
        this.exports[modname] = {};
        console.log(n);
        for (var i = 0; i < n; i++) {
            var name = names[i];
            var attr = module[name];
            var type = typeof attr;
            if (type === "function") {
                var view_name = name + "View";
                var model_name = name + "Model";
                var argnames = this.get_arg_names(attr);
                var modelcls = class extends base.DOMWidgetModel {
                    defaults() {
                        return _.extend({}, base.DOMWidgetModel.prototype.defaults(), {
                            _view_name: view_name,
                            _model_name: model_name
                        });
                    }
                };
                var viewcls = class extends base.DOMWidgetView {
                    render() {
                        var args;
                        var n = argnames.length;
                        for (var i = 0; i < n; i++) {
                            var name = argnames[i];
                            args[name] = this.model.get(name);
                        }
                        this.args = args;
                        this.obj = new this.func(this.args);
                        this.el = this.obj;
                    }
                };
                this.exports[modname][view_name] = viewcls;
                this.exports[modname][model_name] = modelcls;
            }
        }
    }

    get_arg_names(func) {
        var strfn = func.toString().replace(/((\/\/.*$)|(\/\/*[\s\S]*?\*\/))/mg, "");
        var result = strfn.slice(strfn.indexOf("(") + 1, strfn.indexOf(")")).match(/([^\s,]+)/g);
        if (result === null) {
            result = [];
        }
        return result;
    }
}


class APIBuilderModel extends base.WidgetModel {
    defauts() {
        return _.extend({}, base.WidgetModel.prototype.defaults(), {
            _model_name: "APIBuilderModel",
            _view_name: "APIBuilderView"
        });
    }
}


module.exports = {
    APIBuilderView: APIBuilderView,
    APIBuilderModel: APIBuilderModel
};
