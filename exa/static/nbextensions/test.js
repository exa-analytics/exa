/*"""
===============
test.js
===============
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/app': {
            exports: 'app'
        },

        'nbextensions/exa/gui': {
            exports: 'gui'
        },

        'nbextensions/exa/field': {
            exports: 'field'
        },
    },
});


define([
    'nbextensions/exa/app',
    'nbextensions/exa/gui',
    'nbextensions/exa/field'
], function(app, gui, field) {
    var ScalarField = field.ScalarField;
    var sphere = field.sphere;

    class TestGUI extends gui.ContainerGUI {
        constructor(view) {
            super({view: view, autoPlace: false, width: view.gui_width});
        };

        init() {
            var self = this;
            this.buttons = {
                'run all tests': function() {
                    console.log('run all clicked');
                    self.run_all_tests();
                },
            };
            this.run_all = this.add(this.buttons, 'run all tests');
        };

        run_all_tests() {
            console.log('running all tests');
        };
    };

    class TestApp extends app.BaseApp {
        constructor(view) {
            super(view, new TestGUI(view));
            this.field = new ScalarField({
                xmin: 0, xmax: 10, nx: 11,
                ymin: 0, ymax: 10, ny: 11,
                zmin: 0, zmin: 10, nz: 11
            }, sphere);
            var field = this.field.make_field();
            console.log(field);
        };

    };

    return {TestApp: TestApp};
});
