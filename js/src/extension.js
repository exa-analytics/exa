"use strict";
//
//
/* Notebook Extension
 * @desc This file contains the JavaScript that is executed when a notebook is loaded.
 *
 */
//var name = require("../package.json").name;
//
//
//if (window.require) {
//    window.require.config({
//        map: {
//            "*" : {
//                name: "nbextensions/".concat(name).concat("/index")
//            }
//        }
//    });
//}
//
//
//export.exports = {'load_ipython_extensions': function() {}};
exports.__esModule = true;
var base_1 = require("@jupyter-widgets/base");
var WIDGET_EXPORTS = require("./widget");
var version_1 = require("./version");
var EXTENSION_ID = 'jupyter.extensions.exa2';
/**
 * The example plugin.
 */
var examplePlugin = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true
};
exports["default"] = examplePlugin;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: 'exa2',
        version: version_1.JUPYTER_EXTENSION_VERSION,
        exports: WIDGET_EXPORTS
    });
}
