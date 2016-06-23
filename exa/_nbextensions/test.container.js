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
    class TestApp {
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
            this.view.send({'type': 'message', 'app': 'TestApp', 'content': 'True', 'data': 'None'});
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

                'test phong': function() {
                    self.app3d.remove_meshes(self.meshes);
                    self.meshes = self.app3d.test_mesh(true);
                },
            };
            this.level0.clear_button = this.gui.add(this.level0, 'clear');
            this.level0.test_mesh_button = this.gui.add(this.level0, 'test mesh');
            this.level0.test_phong_button = this.gui.add(this.level0, 'test phong');

            this.fields = this.gui.addFolder('fields');
            this.fields['field type'] = '';
            this.fields['dx'] = 0.5;
            this.fields['xmin'] = -2.0;
            this.fields['xmax'] = 2.0;
            this.fields['dy'] = 0.5;
            this.fields['ymin'] = -2.0;
            this.fields['ymax'] = 2.0;
            this.fields['dz'] = 0.5;
            this.fields['zmin'] = -2.0;
            this.fields['zmax'] = 2.0;
            this.fields['isovalue'] = 0.03;
            this.fields['dual'] = false;
            this.fields['field_type_dropdown'] = this.fields.add(this.fields, 'field type', num.function_list_3d);
            this.fields['isovalue_slider'] = this.fields.add(this.fields, 'isovalue', 0.0, 2.0);
            this.fields['dual_checkbox'] = this.fields.add(this.fields, 'dual');
            this.fields['dx_slider'] = this.fields.add(this.fields, 'dx', 0.05, 1.0);
            this.fields['xmin_slider'] = this.fields.add(this.fields, 'xmin', -5.0, 5.0);
            this.fields['xmax_slider'] = this.fields.add(this.fields, 'xmax', -5.0, 5.0);
            this.fields['dy_slider'] = this.fields.add(this.fields, 'dy', 0.05, 1.0);
            this.fields['ymin_slider'] = this.fields.add(this.fields, 'ymin', -5.0, 5.0);
            this.fields['ymax_slider'] = this.fields.add(this.fields, 'ymax', -5.0, 5.0);
            this.fields['dz_slider'] = this.fields.add(this.fields, 'dz', 0.05, 1.0);
            this.fields['zmin_slider'] = this.fields.add(this.fields, 'zmin', -5.0, 5.0);
            this.fields['zmax_slider'] = this.fields.add(this.fields, 'zmax', -5.0, 5.0);
            this.fields.dimensions = {
                'xmin': this.fields.xmin,
                'xmax': this.fields.xmax,
                'ymin': this.fields.ymin,
                'ymax': this.fields.ymax,
                'zmin': this.fields.zmin,
                'zmax': this.fields.zmax,
                'dx': this.fields.dx,
                'dy': this.fields.dy,
                'dz': this.fields.dz
            };

            this.fields.field_type_dropdown.onFinishChange(function(field_type) {
                self.app3d.remove_meshes(self.meshes);
                self.fields['field type'] = field_type;
                self.fields.field = new field.ScalarField(self.fields.dimensions, num[field_type]);
                self.render_field();
            });

            this.fields.dual_checkbox.onChange(function(value) {
                self.fields.dual = value;
                self.fields.sides = self.fields.dual + 1;    //e.g. true + 1 === 2
                self.render_field();
            });

            this.fields.isovalue_slider.onFinishChange(function(value) {
                self.fields.isovalue = value;
                self.render_field();
            });

            this.fields.dx_slider.onFinishChange(function(value) {
                self.fields.dx = value;
                self.fields.field.new_dr({'dx': value});
                self.render_field();
            });

            this.fields.dy_slider.onFinishChange(function(value) {
                self.fields.dy = value;
                self.fields.field.new_dr({'dy': value});
                self.render_field();
            });

            this.fields.dz_slider.onFinishChange(function(value) {
                self.fields.dz = value;
                self.fields.field.new_dr({'dz': value});
                self.render_field();
            });

            this.fields.xmin_slider.onFinishChange(function(value) {
                self.fields.xmin = value;
                self.fields.field.new_limits({'xmin': value});
                self.render_field();
            });

            this.fields.ymin_slider.onFinishChange(function(value) {
                self.fields.ymin = value;
                self.fields.field.new_limits({'ymin': value});
                self.render_field();
            });

            this.fields.zmin_slider.onFinishChange(function(value) {
                self.fields.zmin = value;
                self.fields.field.new_limits({'zmin': value});
                self.render_field();
            });

            this.fields.xmax_slider.onFinishChange(function(value) {
                self.fields.xmax = value;
                self.fields.field.new_limits({'xmax': value});
                self.render_field();
            });

            this.fields.ymax_slider.onFinishChange(function(value) {
                self.fields.ymax = value;
                self.fields.field.new_limits({'ymax': value});
                self.render_field();
            });

            this.fields.zmax_slider.onFinishChange(function(value) {
                self.fields.zmax = value;
                self.fields.field.new_limits({'zmax': value});
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

    return TestApp;
});
