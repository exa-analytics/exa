// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
=================
base.js
=================
JavaScript "frontend" complement of exawidget's Container for use within
the Jupyter notebook interface. This "module" standardizes bidirectional
communication logic for all container widget views.

The structure of the frontend is to generate an HTML widget ("container" - see
create_container) and then populate its canvas with an application ("app")
appropriate to the type of container. If the (backend) container is empty, then
populate the HTML widget with the test application.
*/
//"use strict";
//var widgets = require("jupyter-js-widgets");
//var _ = require("underscore");
////var field = require("./field.js");
////var app3d = require("./app3d.js");
////var num = require("./num.js");
//
//class BaseDataModel extends widgets.WidgetModel {
//    get defaults() {
//        return _.extend({}, widgets.WidgetModel.prototype.defaults, {
//            _model_module: "jupyter-exawidgets",
//            _view_module: "jupyter-exawidgets",
//            _model_name: "BaseDataModel",
//            _view_name: "BaseDataView"
//        })
//    }
//}
//
//class BaseDataView extends widgets.WidgetView {
//}
//
//class BaseDOMModel extends widgets.DOMWidgetModel {
//
//    get defaults() {
//        return _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
//            _model_module: "jupyter-exawidgets",
//            _view_module: "jupyter-exawidgets",
//            _model_name: "BaseDOMModel",
//            _view_name: "BaseDOMView"
//        })
//    }
//
//    clear() {
//        if (this.get("background") === "green") {
//            this.set("background", "black");
//        } else {
//            this.set("background", "green");
//        }
//    }
//
//}
//
//class BaseDOMView extends widgets.DOMWidgetView {
//
//    initialize() {
//        widgets.DOMWidgetView.prototype.initialize.apply(this, arguments);
//        var that = this;
//        $(this.el).width(
//            this.model.get("layout").get("width")).height(
//            this.model.get("layout").get("height")).resizable({
//            aspectRatio: false,
//            resize: function(event, ui) {
//                var w = ui.size.width;
//                var h = ui.size.height;
//                that.model.get("layout").set("width", w);
//                that.model.get("layout").set("height", h);
//                that.el.width = w;
//                that.el.height = h;
//                that.resize(w, h);
//            }
//        });
//        this.init();
//    }
//
//    init() {
//        this.init_listeners();
//    }
//
//    init_listeners() {
//        this.model.on("change:background", this.set_background, this);
//    }
//
//    set_buttons() {
//        var that = this;
//        var clear = document.createElement("button");
//        clear.classList.add("jupyter-widgets");
//        clear.classList.add("jupyter-button");
//        clear.classList.add("widget-toggle-button");
//        clear.setAttribute("data-toggle", "tooltip");
//        clear.setAttribute("title", "Clear");
//        clear.onclick = function(e) {
//            e.preventDefault();
//            that.model.clear();
//        };
//        var icon = document.createElement("i");
//        icon.className = "fa fa-arrows";
//        clear.appendChild(icon);
//        this.el.appendChild(clear);
//    }
//
//    set_background() {
//        this.$el.css({"background-color": this.model.get("background")});
//    }
//
//    render() {
//        this.set_buttons();
//        this.set_background();
//    }
//
//    resize(w, h) {
//    }
//
//}
//
//
//class BaseBoxModel extends widgets.BoxModel {
//    get defaults() {
//        return _.extend({}, widgets.BoxModel.prototype.defaults, {
//            _model_module: "jupyter-exawidgets",
//            _view_module: "jupyter-exawidgets",
//            _model_name: "BaseBoxModel",
//            _view_name: "BaseBoxView"
//        })
//    }
//}
//
//
//class BaseBoxView extends widgets.BoxView {
//    render() {
//        console.log("base box view render");
//        super.render();
//    }
//}
//
//
//module.exports = {
//    BaseDataModel: BaseDataModel,
//    BaseDataView: BaseDataView,
//    BaseDOMModel: BaseDOMModel,
//    BaseDOMView: BaseDOMView,
//    BaseBoxModel: BaseBoxModel,
//    BaseBoxView: BaseBoxView
//}
