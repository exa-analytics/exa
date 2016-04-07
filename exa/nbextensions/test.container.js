/*"""
===================================
container.test.js
===================================
A test application called when an empty container widget is rendered in a
Jupyter notebook environment.
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/apps/app3d': {
            exports: 'App3D'
        },

        'nbextensions/exa/apps/gui': {
            exports: 'ContainerGUI'
        },

        'nbextensions/exa/num': {
            exports: 'num'
        },

        'nbextensions/exa/field': {
            exports: 'field'
        },
    },
});


define([
    'nbextensions/exa/apps/app3d',
    'nbextensions/exa/apps/gui',
    'nbextensions/exa/num',
    'nbextensions/exa/field'
], function(App3D, ContainerGUI, num, field) {
    class TestContainer {
        /*"""
        TestContainer
        ==============
        A test application for the container
        */
        constructor(view) {
            this.view = view;
            this.view.create_canvas();
            this.meshes = [];
            this.app3d = new App3D(this.view.canvas);
            this.create_gui();
            this.view.container.append(this.gui.domElement);
            this.view.container.append(this.gui.custom_css);
            this.view.container.append(this.view.canvas);
            var view_self = this.view;
            this.app3d.render();
            this.view.on('displayed', function() {
                view_self.app.app3d.animate();
                view_self.app.app3d.controls.handleResize();
            });
        };

        create_gui() {
            /*"""
            create_gui
            ------------
            Creates the gui
            */
            var self = this;
            this.gui = new ContainerGUI(this.view.gui_width);

            // GUI levels are the heirarchy of folders in dat gui 0: top level
            this.level0 = {
                'clear': function() {
                    self.app3d.remove_meshes(self.meshes);
                },

                'test mesh': function() {
                    self.app3d.remove_meshes(self.meshes);
                    self.meshes = self.app3d.test_mesh();
                },
            };
            this.level0.clear_button = this.gui.add(this.level0, 'clear');
            this.level0.test_mesh_button = this.gui.add(this.level0, 'test mesh');

            this.fields = this.gui.addFolder('fields');
            this.fields['field type'] = '';
            this.fields['dx'] = 0.5;
            this.fields['xmin'] = -5.0;
            this.fields['xmax'] = 5.0;
            this.fields['dy'] = 0.5;
            this.fields['ymin'] = -5.0;
            this.fields['ymax'] = 5.0;
            this.fields['dz'] = 0.5;
            this.fields['zmin'] = -5.0;
            this.fields['zmax'] = 5.0;
            this.fields['isovalue'] = 0.03;
            this.fields['dual'] = false;
            this.fields['isovalue_slider'] = this.fields.add(this.fields, 'isovalue', 0.0, 2.0);
            this.fields['dual_checkbox'] = this.fields.add(this.fields, 'dual');
            this.fields['dx_slider'] = this.fields.add(this.fields, 'dx', 0.01, 10.0);
            this.fields['xmin_slider'] = this.fields.add(this.fields, 'xmin', -50.0, 50.0);
            this.fields['xmax_slider'] = this.fields.add(this.fields, 'xmax', -50.0, 50.0);
            this.fields['dy_slider'] = this.fields.add(this.fields, 'dy', 0.01, 10.0);
            this.fields['ymin_slider'] = this.fields.add(this.fields, 'ymin', -50.0, 50.0);
            this.fields['ymax_slider'] = this.fields.add(this.fields, 'ymax', -50.0, 50.0);
            this.fields['dz_slider'] = this.fields.add(this.fields, 'dz', 0.01, 10.0);
            this.fields['zmin_slider'] = this.fields.add(this.fields, 'zmin', -50.0, 50.0);
            this.fields['zmax_slider'] = this.fields.add(this.fields, 'zmax', -50.0, 50.0);
            this.fields['field_type_dropdown'] = this.fields.add(this.fields, 'field type', num.function_list_3d);

            this.fields.field_type_dropdown.onFinishChange(function(field_type) {
                self.app3d.remove_meshes(self.meshes);
                self.fields['field type'] = field_type;
                self.fields.dimensions = {
                    'xmin': self.fields.xmin,
                    'xmax': self.fields.xmax,
                    'ymin': self.fields.ymin,
                    'ymax': self.fields.ymax,
                    'zmin': self.fields.zmin,
                    'zmax': self.fields.zmax,
                    'dx': self.fields.dx,
                    'dy': self.fields.dy,
                    'dz': self.fields.dz
                };
                self.fields.field = new field.ScalarField(self.fields.dimensions, num[field_type]);
                self.render_field();
            });

            this.fields.dual_checkbox.onChange(function(value) {
                console.log(value);
                self.fields.dual = value;
                self.fields.sides = self.fields.dual + 1;
                console.log(self.fields.sides);
                self.render_field();
            });

            this.fields.isovalue_slider.onFinishChange(function(value) {
                self.fields.isovalue = value;
                self.fields.field = new field.ScalarField(self.fields.dimensions, num[self.fields['field type']]);
                self.render_field();
            });
        };

        resize() {
            this.app3d.resize();
        };

        render_field() {
            this.app3d.remove_meshes(this.meshes);
            this.meshes = this.app3d.add_scalar_field(this.fields.field, this.fields.isovalue, this.fields.sides);
            this.app3d.set_camera_from_mesh(this.meshes[0]);
        };
    };

    return TestContainer;
});
