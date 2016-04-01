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
            this.ymay = dimensions.ymax;
            this.ny = dimensions.ny;
            this.zmin = dimensions.zmin;
            this.zmaz = dimensions.zmax;
            this.nz = dimensions.nz;
            this.update_x();
            this.update_y();
            this.update_z();
        };

        update_x() {
            this.xarray = num.linspace(this.xmin, this.xmax, this.nx);
        };

        update_y() {
            this.yarray = num.linspace(this.ymin, this.ymax, this.ny);
        };

        update_z() {
            this.zarray = num.linspace(this.zmin, this.zmax, this.nz);
        };

        make_field() {
            this.field = new Float32Array(this.nx * this.ny * this.nz);
            var h = 0;
            for (let x of this.xarray) {
                for (let y of this.yarray) {
                    for (let z of this.zarray) {
                        this.field[h] = this.func(x, y, z);
                        h += 1;
                    };
                };
            };
            return this.field;
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
