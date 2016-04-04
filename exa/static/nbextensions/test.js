/*"""
===============
test.js
===============
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/app.three': {
            exports: 'app3d'
        },
        'nbextensions/exa/app.gui': {
            exports: 'gui'
        },

        'nbextensions/exa/field': {
            exports: 'field'
        },
    },
});


define([
    'nbextensions/exa/app.three',
    'nbextensions/exa/app.gui',
    'nbextensions/exa/field'
], function(app3d, gui, field) {
    class TestGUI extends gui.ContainerGUI {
        /*"""
        */
        init() {
            var self = this;
            this.buttons = {
                'run all tests': function() {
                    console.log('run all clicked');
                    self.run_all_tests();
                },
            };
            this.run_all = this.ui.add(this.buttons, 'run all tests');
        };

        run_all_tests() {
            console.log('running all tests');
        };
    };

    class TestApp {
        constructor(view) {
            this.view = view;
            this.gui = new TestGUI(this.view);
            this.app3d = new app3d.ThreeJSApp(this.view.canvas);
            this.field = new field.ScalarField({
                xmin: -1.0, xmax: 1.0, dx: 1.0,
                ymin: -1.0, ymax: 1.0, dy: 1.0,
                zmin: -1.0, zmax: 1.0, dz: 1.0
            }, field.sphere);
            //this.points = this.app3d.add_points(this.field.x, this.field.y, this.field.z);
            //this.app3d.set_camera_from_mesh(this.points);
            console.log(this.field.values);
            console.log(this.field.values.length);
            this.field_mesh = this.app3d.add_single_scalar_field(this.field, 0);
            this.app3d.set_camera();
        };

        resize() {
            this.app3d.resize();
        };

        func() {
            for (let i=0; i<10; i++) {
                console.log('inner i' + i.toString());
            };
        };
    };

    return {TestApp: TestApp};
});
