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
var jupyterWidgetsBase = require("@jupyter-widgets/base");
var builder = require("./builder");
var three = require("three");
console.log(jupyterWidgetsBase);
var TestWidgetView = /** @class */ (function (_super) {
    __extends(TestWidgetView, _super);
    function TestWidgetView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return TestWidgetView;
}(jupyterWidgetsBase.WidgetView));
exports.TestWidgetView = TestWidgetView;
var TestWidgetModel = /** @class */ (function (_super) {
    __extends(TestWidgetModel, _super);
    function TestWidgetModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TestWidgetModel.prototype.initialize = function () {
        console.log("init");
        _super.prototype.initialize.call(this, this, arguments);
        var pkgs = {};
        console.log("Building API synchronously");
        pkgs['three'] = builder.build(three);
        console.log(pkgs);
    };
    TestWidgetModel.prototype.defaults = function () {
        return __assign({}, _super.prototype.defaults.call(this), {
            '_view_name': "TestWidgetView",
            '_view_module': "exa",
            '_view_module_version': "^0.4.0",
            '_model_name': "TestWidgetModel",
            '_model_module': "exa",
            '_model_module_version': "^0.4.0"
            //'value': "Hello World",
        });
    };
    return TestWidgetModel;
}(jupyterWidgetsBase.WidgetModel));
exports.TestWidgetModel = TestWidgetModel;
