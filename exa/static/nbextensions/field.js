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
        constructor(dimensions, func_or_values) {
            /*"""
            ScalarField
            =============
            A class to contain a scalar field

            Args:
                dimensions (array): List of dimensions specifying the construction of the field
                func (function): Function of 3D space

            Note:
                The dimensions argument should be a dictionary of the form
                {xmin: xmin, xmax: xmax, nx: nx, ymin: ymin, ...}
            */
            console.log('scalar fielding');
            this.func;
            this.values;
            this.xmin = dimensions.xmin;
            this.xmax = dimensions.xmax;
            this.nx = dimensions.nx;
            this.dx = dimensions.dx;
            this.ymin = dimensions.ymin;
            this.ymax = dimensions.ymax;
            this.ny = dimensions.ny;
            this.dy = dimensions.dy;
            this.zmin = dimensions.zmin;
            this.zmax = dimensions.zmax;
            this.nz = dimensions.nz;
            this.dz = dimensions.dz;
            if (typeof func_or_values === 'function') {
                console.log('Building field from function');
                console.log(func_or_values);
                this.func = func_or_values;
                this.update_x();
                this.update_y();
                this.update_z();
                this.update_field();
            } else {
                console.log('NotImplementedError(Field values are not yet supported)');
            };
        };

        update_x() {
            if (this.dx === undefined) {
                this.x = num.linspace(this.xmin, this.xmax, this.nx);
            } else {
                this. x = num.arange(this.xmin, this.xmax, this.dx);
            };
        };

        update_y() {
            if (this.dy === undefined) {
                this.y = num.linspace(this.ymin, this.ymax, this.ny);
            } else {
                this.y = num.arange(this.ymin, this.ymax, this.dy);
            };
        };

        update_z() {
            if (this.dz === undefined) {
                this.z = num.linspace(this.zmin, this.zmax, this.nz);
            } else {
                this.z = num.arange(this.zmin, this.zmax, this.dz);
            };
        };

        update_field() {
            this.values = [];
            for (let x of this.x) {
                for (let y of this.y) {
                    for (let z of this.z) {
//                        console.log(x.toString() + ' ' + y.toString() + ' ' + z.toString());
                        this.values.push(this.func(x, y, z));
                    };
                };
            };
        };
    };

    var sphere = function(x, y, z) {
        return x * x + y * y + z * z - 1.0;
    };

    return {
        ScalarField: ScalarField,
        sphere: sphere
    };
});
