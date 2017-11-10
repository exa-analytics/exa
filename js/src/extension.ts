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

import {
  Application, IPlugin
} from '@phosphor/application';

import {
  Widget
} from '@phosphor/widgets';

import {
  IJupyterWidgetRegistry
 } from '@jupyter-widgets/base';

import * as WIDGET_EXPORTS from './widget';

import {
  JUPYTER_EXTENSION_VERSION
} from './version';


const EXTENSION_ID = 'jupyter.extensions.exa2';


/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default examplePlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: 'exa2',
    version: JUPYTER_EXTENSION_VERSION,
    exports: WIDGET_EXPORTS
  });
}
