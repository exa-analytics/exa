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
var ipywidgets = require("@jupyter-widgets/base");
var builder = require("./builder.js");
var three = require("three");
if (typeof (Worker) === "undefined") {
    console.log("Building API using workers");
    worker = new Worker("./builder.js");
    worker.postMessage({ 'mod': three });
}
else {
    console.log("Building API slowly");
    builder.build(three);
}
var TestWidgetView = /** @class */ (function (_super) {
    __extends(TestWidgetView, _super);
    function TestWidgetView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TestWidgetView.prototype.render = function () {
        console.log("hereererere! ");
        console.log(this.model.get("value"));
        this.el.textContent = this.model.get("value");
    };
    return TestWidgetView;
}(ipywidgets.DOMWidgetView));
exports.TestWidgetView = TestWidgetView;
var TestWidgetModel = /** @class */ (function (_super) {
    __extends(TestWidgetModel, _super);
    function TestWidgetModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TestWidgetModel.prototype.defaults = function () {
        return __assign({}, _super.prototype.defaults.call(this), {
            '_view_name': "TestWidgetView",
            '_view_module': "jupyter-exa",
            '_view_module_version': "^0.4.0",
            '_model_name': "TestWidgetModel",
            '_model_module': "jupyter-exa",
            '_model_module_version': "^0.4.0",
            'value': "Hello World"
        });
    };
    return TestWidgetModel;
}(ipywidgets.DOMWidgetModel));
exports.TestWidgetModel = TestWidgetModel;
