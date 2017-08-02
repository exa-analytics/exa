// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * This module provides the base model and view used by
 * exa.core.widget.DOMWidget.
 * @module
 */
"use strict";
var ipyw = require("jupyter-js-widgets");
var _ = require("underscore");
var jsver = "^0.4.0";
var jsmod = "jupyter-exa";


class HelloModel extends ipyw.DOMWidgetModel {
    get defaults() {
        return _.extend(ipyw.DOMWidgetModel.prototype.defaults(), {
            _model_name: "HelloModel",
            _model_module: jsmod,
            _model_version: jsver,
            _view_name: "HelloView",
            _view_module: jsmod,
            _view_version: jsver,
            value: "Hello World"
        });
    }
}


class HelloView extends ipyw.DOMWidgetView {
    render() {
        this.value_changed();
        this.model.on("change:value", this.value_changed, this);
    }

    value_changed() {
        this.el.textContext = this.model.get("value");
    }
}


module.exports = {
    HelloModel: HelloModel,
    HelloView: HelloView
};


//var ipyw = require("@jupyter-widgets/base");
//var _ = require("underscore");
//var jsver = "^0.4.0";
//var jsmod = "jupyter-exa";
//
//
///**
// * Base Model Class
// */
//class WidgetModel extends ipyw.WidgetModel {
//    get defaults() {
//        return _.extend({}, ipyw.WidgetModel.prototype.defaults, {
//            _view_name: "WidgetView",
//            _view_module: jsmod,
//            _view_module_version: jsver,
//            _model_name: "WidgetModel",
//            _model_module: jsmod,
//            _model_module_version: jsver
//        });
//    }
//}
//
//
///**
// * Base View Class
// */
//class WidgetView extends ipyw.WidgetView {
//}
//
//
///**
// * Base (DOM) Model Class
// */
//class DOMWidgetModel extends ipyw.DOMWidgetModel {
//    /**
//     * Used by Jupyter
//     */
//    get defaults() {
//        return _.extend({}, ipyw.DOMWidgetModel.prototype.defaults, {
//            _view_name: "DOMWidgetView",
//            _view_module: jsmod,
//            _view_module_version: jsver,
//            _model_name: "DOMWidgetModel",
//            _model_module: jsmod,
//            _model_module_version: jsver
//        });
//    }
//}
//
//
///**
// * Base (DOM) View Class
// */
//class DOMWidgetView extends ipyw.DOMWidgetView {
//}
//
//
//module.exports = {
//    jsver: jsver,
//    jsmod: jsmod,
//    WidgetModel: WidgetModel,
//    WidgetView: WidgetView,
//    DOMWidgetModel: DOMWidgetModel,
//    DOMWidgetView: DOMWidgetView
//};
