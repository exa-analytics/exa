// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
test.js
##############
A test application called when an empty container widget is rendered in a
Jupyter notebook environment.
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/app3d': {exports: 'App3D'},
        'nbextensions/exa/gui': {exports: 'ContainerGUI'},
        'nbextensions/exa/num': {exports: 'num'},
        'nbextensions/exa/field': {exports: 'field'},
    },
});


define([
    'nbextensions/exa/app3d',
    'nbextensions/exa/gui',
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
            this.view.send({'type': 'message',
                            'app': 'TestApp',
                            'content': 'True',
                            'data': 'test app message'});
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
            this.top = {
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
            this.top.clear_button = this.gui.add(this.top, 'clear');
            this.top.test_mesh_button = this.gui.add(this.top, 'test mesh');
            this.top.test_phong_button = this.gui.add(this.top, 'test phong');

            this.fields = {
                'nx': 13, 'ny': 13, 'nz': 13,
                'isovalue': 1.0, 'boxsize': 3,
                'ox': -3.0, 'oy': -3.0, 'oz': -3.0,
                'fx':  3.0, 'fy':  3.0, 'fz':  3.0,
                'dxi': 0.5, 'dyj': 0.5, 'dzk': 0.5,
                'dxj': 0.0, 'dyi': 0.0, 'dzi': 0.0,
                'dxk': 0.0, 'dyk': 0.0, 'dzj': 0.0,
                'field type': null
            };
            this.fields['folder'] = this.gui.addFolder('fields');
            this.fields['isovalue_slider'] = this.fields.folder.add(this.fields, 'isovalue', 0.1, 10.0);
            this.fields['field_type_dropdown'] = this.fields.folder.add(this.fields, 'field type', num.function_list_3d);
            this.fields['boxsize_slider'] = this.fields.folder.add(this.fields, 'boxsize', 3, 5);
            this.fields['nx_slider'] = this.fields.folder.add(this.fields, 'nx').min(5).max(25).step(1);
            this.fields['ny_slider'] = this.fields.folder.add(this.fields, 'ny').min(5).max(25).step(1);
            this.fields['nz_slider'] = this.fields.folder.add(this.fields, 'nz').min(5).max(25).step(1);
            this.fields.field_type_dropdown.onFinishChange(function(field_type) {
                self.fields['field type'] = field_type;
                self.fields.field = new field.ScalarField(self.fields, num[field_type]);
                self.render_field();
            });
            this.fields.isovalue_slider.onFinishChange(function(value) {
                self.fields.isovalue = value;
                self.render_field();
            });
            this.fields.boxsize_slider.onFinishChange(function(value) {
                self.fields.ox = -value;
                self.fields.fx = value;
                self.fields.oy = -value;
                self.fields.fy = value;
                self.fields.oz = -value;
                self.fields.fz = value;
                self.fields.field.x = num.linspace(self.fields.ox, self.fields.fx, self.fields.nx);
                self.fields.field.y = num.linspace(self.fields.oy, self.fields.fy, self.fields.ny);
                self.fields.field.z = num.linspace(self.fields.oz, self.fields.fz, self.fields.nz);
                self.fields.field.update();
                self.render_field();
            });
            this.fields.nx_slider.onFinishChange(function(value) {
                self.fields.nx = value;
                self.fields.field.x = num.linspace(self.fields.ox,
                                                   self.fields.fx,
                                                   self.fields.nx);
                self.fields.field.update();
                self.render_field();
            });
            this.fields.ny_slider.onFinishChange(function(value) {
                self.fields.ny = value;
                self.fields.field.y = num.linspace(self.fields.oy,
                                                   self.fields.fy,
                                                   self.fields.ny);
                self.fields.field.update();
                self.render_field();
            });
            this.fields.nz_slider.onFinishChange(function(value) {
                self.fields.nz = value;
                self.fields.field.z = num.linspace(self.fields.oz,
                                                   self.fields.fz,
                                                   self.fields.nz);
                self.fields.field.update();
                self.render_field();
            });
        };

        resize() {
            this.app3d.resize();
        };

        render_field() {
            this.app3d.remove_meshes(this.meshes);
            console.log('rendering field with arrays array dimensions');
            console.log('x length', this.fields.field.x.length);
            console.log('y length', this.fields.field.y.length);
            console.log('z length', this.fields.field.z.length);
            this.meshes = this.app3d.add_scalar_field(this.fields.field, this.fields.isovalue, this.fields.sides);
            this.app3d.set_camera({'x': 5.0, 'y': 5.0, 'z': 5.0});
        };
    };

    return TestApp;
});
