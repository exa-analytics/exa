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
var pkgdata = {};
function onmessage(e) {
    console.log("onmessage");
    build(e.mod);
}
function _proto_helper(obj) {
    if (obj == null)
        return;
    _proto_helper(Object.getPrototypeOf(obj));
}
function get_proto_names(obj) {
    var names = [];
    for (; obj != null; obj = Object.getPrototypeOf(obj)) {
        var op = Object.getOwnPropertyNames(obj);
        for (var i = 0; i < op.length; i++) {
            if (names.indexOf(op[i]) == -1) {
                names.push(op[i]);
            }
        }
    }
    return names;
}
function build_mv(viewname, modelname, obj) {
    var attrnames = get_proto_names(obj);
    var Model = /** @class */ (function (_super) {
        __extends(Model, _super);
        function Model() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Model.prototype.defaults = function () {
            return __assign({}, _super.prototype.defaults.call(this), {
                '_view_name': viewname,
                '_view_module': "jupyter-exa",
                '_view_module_version': "^0.4.0",
                '_model_name': modelname,
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
    return { 'model': Model, 'view': View, 'attrnames': attrnames };
}
function build(mod) {
    console.log("In build...");
    console.log(mod);
    var pydata = {};
    for (var _i = 0, _a = Object.getOwnPropertyNames(mod); _i < _a.length; _i++) {
        var name = _a[_i];
        console.log("building: ".concat(name));
        var viewname = name.concat("View");
        var modelname = name.concat("Model");
        var obj = mod[name];
        var mv = build_mv(viewname, modelname, obj);
        pkgdata[viewname] = mv.view;
        pkgdata[modelname] = mv.model;
        pydata[name] = mv.attrnames;
        console.log("done with: ".concat(name));
    }
    ;
    return pydata;
}
exports.build = build;
for (var _i = 0, pkgdata_1 = pkgdata; _i < pkgdata_1.length; _i++) {
    var name = pkgdata_1[_i];
    name = pkgdata[name];
}
