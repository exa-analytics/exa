"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
exports.__esModule = true;
// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
var ipywidgets = require("@jupyter-widgets/base");
var pkgdata = {};
function onmessage(e) {
    console.log("onmessage");
    build(e.mod);
}
function getProtoNames(obj) {
    var names = [];
    for (; obj != null; obj = Object.getPrototypeOf(obj)) {
        var op = Object.getOwnPropertyNames(obj);
        for (var i = 0; i < op.length; i++) {
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
    var Model = /** @class */ (function (_super) {
        __extends(Model, _super);
        function Model() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Model.prototype.defaults = function () {
            return __assign({}, _super.prototype.defaults.call(this), {
                '_view_name': viewName,
                '_view_module': "jupyter-exa",
                '_view_module_version': "^0.4.0",
                '_model_name': modelName,
                '_model_module': "jupyter-exa",
                '_model_module_version': "^0.4.0"
            });
        };
        return Model;
    }(ipywidgets.DOMWidgetModel));
    var View = /** @class */ (function (_super) {
        __extends(View, _super);
        function View() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        View.prototype.render = function () {
            console.log("Dynamic rendering.");
        };
        return View;
    }(ipywidgets.DOMWidgetView));
    return { 'model': Model, 'view': View, 'attrNames': attrNames };
}
function build(mod) {
    console.log("In build...");
    //console.log(mod);
    var pydata = {};
    for (var _i = 0, _a = Object.getOwnPropertyNames(mod); _i < _a.length; _i++) {
        var name = _a[_i];
        //console.log("building: ".concat(name));
        var viewName = name.concat("View");
        var modelName = name.concat("Model");
        var obj = mod[name];
        var mv = buildModelView(viewName, modelName, obj);
        pkgdata[viewName] = mv.view;
        pkgdata[modelName] = mv.model;
        pydata[name] = mv.attrNames;
        //console.log("done with: ".concat(name));
    }
    ;
    for (var _b = 0, pkgdata_1 = pkgdata; _b < pkgdata_1.length; _b++) {
        var name = pkgdata_1[_b];
        console.log(name);
        name = pkgdata[name];
    }
    return pydata;
}
exports.build = build;
