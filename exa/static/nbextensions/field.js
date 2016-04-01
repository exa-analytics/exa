/*"""
===============
volume.js
===============
Functions for creating discrete volume data (3D spatial data) from analytical
functions.
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/num': {
            exports: 'num'
        },
    },
});


define([
    'nbextensions/exa/num',
], function(num) {
    class ScalarField {
        constructor(dimensions, func) {
            /*"""
            ScalarField
            =============
            A class to contain a scalar field

            Args:
                dimensions (array): List of dimensions specifying the construction of the field
                func (function): Function of 3D space

            Note:
                The dimensions should be of the form [[xmin, xmax, nx], [...], [...]].
            */
            this.func = func;
            this.xmin = dimensions.xmin;
            this.xmax = dimensions.xmax;
            this.nx = dimensions.nx;
            this.ymin = dimensions.ymin;
            this.ymax = dimensions.ymax;
            this.ny = dimensions.ny;
            this.zmin = dimensions.zmin;
            this.zmax = dimensions.zmax;
            this.nz = dimensions.nz;
            this.update_x();
            this.update_y();
            this.update_z();
            this.update_field();
        };

        update_x() {
            this.x = num.linspace(this.xmin, this.xmax, this.nx);
        };

        update_y() {
            this.y = num.linspace(this.ymin, this.ymax, this.ny);
        };

        update_z() {
            this.z = num.linspace(this.zmin, this.zmax, this.nz);
        };

        update_field() {
            this.values = new Float32Array(this.nx * this.ny * this.nz);
            var h = 0;
            for (let x of this.x) {
                for (let y of this.y) {
                    for (let z of this.z) {
                        this.values[h] = this.func(x, y, z);
                        h += 1;
                    };
                };
            };
        };
    };

    var sphere = function(x, y, z) {
        return x^2 + y^2 + z^2;
    };

    return {
        ScalarField: ScalarField,
        sphere: sphere
    };
});
