/*"""
===============
test.js
===============
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/app.gui': {
            exports: 'gui'
        },
    },
});


define([
    'nbextensions/exa/app.gui'
], function(gui) {
    class TestGUI extends gui.ContainerGUI {
        constructor(view) {
            super(view);
        }
    }

    TestGUI.prototype.init = function() {
        var self = this;
        this.buttons = {
            'run all tests': function() {
                console.log('run all clicked');
                self.run_all_tests();
            },
        };
        this.run_all = this.ui.add(this.buttons, 'run all tests');
    };

    var TestApp = function(view) {
        /*"""
        */
        this.view = view;
        this.gui = new TestGUI(this.view);
    };

    return {'TestApp': TestApp};
});
