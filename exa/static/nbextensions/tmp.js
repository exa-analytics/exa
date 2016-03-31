    var ContainerView = widget.DOMWidgetView.extend({
        render: function() {

        /*    this.init_default_model_listeners();

            this.init_container();                    // Second initialize the
            this.init_canvas();                       // application(s).
            this.app = new app3D.ThreeJSApp(this.canvas);
            console.log($);
            console.log(_);
            console.log(_.object);
            this.send('string');
            this.send(1234);
            this.send([1234, 'package']);
            this.send({'key': 'value', 'key2': 'othervalue'});
            this.send({event: 'stuff'});
            this.send({key: 'stuffsz'});
            //this.app.add_points(this.test_x, this.test_y, this.test_z);

            //this.app.test_mesh();    // Simple box geometry three.app.js test
            //this.app.set_camera();

            this.container.append(this.canvas);       // Lastly set the html
            this.setElement(this.container);          // objects and run.
            this.app.render();
            this.on('displayed', function() {
                self.app.animate();
                self.app.controls.handleResize();
            });*/
        },


        init_default_model_listeners: function() {
            /*"""
            init_default_model_listeners
            -------------------------------
            Sets up the frontend to listen to common variables present in the
            backend
            */
            this.update_field_nx();
            this.update_field_ny();
            this.update_field_nz();
            this.update_field_xi();
            this.update_field_xj();
            this.update_field_xk();
            this.update_field_yi();
            this.update_field_yj();
            this.update_field_yk();
            this.update_field_zi();
            this.update_field_zj();
            this.update_field_zk();
            this.update_field_ox();
            this.update_field_oy();
            this.update_field_oz();
            this.update_field_values();
            this.update_field_indices();
            this.model.on('change:field_nx', this.update_field_nx, this);
            this.model.on('change:field_ny', this.update_field_ny, this);
            this.model.on('change:field_nz', this.update_field_nz, this);
            this.model.on('change:field_xi', this.update_field_xi, this);
            this.model.on('change:field_xj', this.update_field_xj, this);
            this.model.on('change:field_xk', this.update_field_xk, this);
            this.model.on('change:field_yi', this.update_field_yi, this);
            this.model.on('change:field_yj', this.update_field_yj, this);
            this.model.on('change:field_yk', this.update_field_yk, this);
            this.model.on('change:field_zi', this.update_field_zi, this);
            this.model.on('change:field_zj', this.update_field_zj, this);
            this.model.on('change:field_zk', this.update_field_zk, this);
            this.model.on('change:field_ox', this.update_field_ox, this);
            this.model.on('change:field_oy', this.update_field_oy, this);
            this.model.on('change:field_oz', this.update_field_oz, this);
            this.model.on('change:field_values', this.update_field_values, this);
            this.model.on('change:field_indices', this.update_field_values, this);
        },



        update_field_nx: function() {
            this.field_nx = this.get_trait('field_nx');
        },

        update_field_ny: function() {
            this.field_ny = this.get_trait('field_ny');
        },

        update_field_nz: function() {
            this.field_nz = this.get_trait('field_nz');
        },

        update_field_xi: function() {
            this.field_xi = this.get_trait('field_xi');
        },

        update_field_xj: function() {
            this.field_xj = this.get_trait('field_xj');
        },

        update_field_xk: function() {
            this.field_xk = this.get_trait('field_xk');
        },

        update_field_yi: function() {
            this.field_yi = this.get_trait('field_yi');
        },

        update_field_yj: function() {
            this.field_yj = this.get_trait('field_yj');
        },

        update_field_yk: function() {
            this.field_yk = this.get_trait('field_yk');
        },

        update_field_zi: function() {
            this.field_zi = this.get_trait('field_zi');
        },

        update_field_zj: function() {
            this.field_zj = this.get_trait('field_zj');
        },

        update_field_zk: function() {
            this.field_zk = this.get_trait('field_zk');
        },

        update_field_ox: function() {
            this.field_ox = this.get_trait('field_ox');
        },

        update_field_oy: function() {
            this.field_oy = this.get_trait('field_oy');
        },

        update_field_oz: function() {
            this.field_oz = this.get_trait('field_oz');
        },

        update_field_values: function() {
            this.field_values = this.get_trait('field_values');
            console.log(this.field_values);
        },

        update_field_indices: function() {
            this.field_indices = this.get_trait('field_indices');
            console.log(this.field_indices);
        },
    });

    return {'ContainerView': ContainerView};
});
