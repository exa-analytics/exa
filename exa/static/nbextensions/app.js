/*"""
===============
app.js
===============
*/
'use strict';

define([], function() {
    class BaseApp {
        constructor(view, gui) {
            this.view = view;
            this.gui = gui;
        };
    };

    return {BaseApp: BaseApp};
});
