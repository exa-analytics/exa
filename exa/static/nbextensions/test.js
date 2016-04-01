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
                xmin: -5, xmax: 5, nx: 11,
                ymin: -5, ymax: 5, ny: 11,
                zmin: -5, zmax: 5, nz: 11
            }, field.sphere);
            console.log(this.field);
            console.log(this.field.values);
            //this.points = this.app3d.add_points(this.field.x, this.field.y, this.field.z);
            //this.app3d.set_camera_from_mesh(this.points);
            this.field_mesh = this.app3d.add_scalar_field(this.field, 3);
            console.log(this.field_mesh);
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
