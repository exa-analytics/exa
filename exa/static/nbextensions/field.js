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
                this.dx = this.x[1] - this.x[0];
            } else {
                this.x = num.arange(this.xmin, this.xmax, this.dx);
                this.nx = this.x.length;
            };
        };

        update_y() {
            if (this.dy === undefined) {
                this.y = num.linspace(this.ymin, this.ymax, this.ny);
                this.dy = this.y[1] - this.y[0];
            } else {
                this.y = num.arange(this.ymin, this.ymax, this.dy);
                this.ny = this.y.length;
            };
        };

        update_z() {
            if (this.dz === undefined) {
                this.z = num.linspace(this.zmin, this.zmax, this.nz);
                this.dz = this.z[1] - this.z[0];
            } else {
                this.z = num.arange(this.zmin, this.zmax, this.dz);
                this.nz = this.z.length;
            };
        };

        update_field() {
            this.values = [];
            for (let x of this.x) {
                for (let y of this.y) {
                    for (let z of this.z) {
                        this.values.push(this.func(x, y, z));
                    };
                };
            };
        };
    };

    var sphere = function(x, y, z) {
        return x * x + y * y + z * z - 0.1;
    };

    var torus = function(x, y, z, c) {
        if (c === undefined) {
            c = 1.0;
        };
        return Math.pow(c - Math.sqrt(x * x + y * y), 2) + z * z;
    };

    var sto = function(x, y, z) {
        return Math.exp(-Math.sqrt(x * x + y * y + z * z));
    };

    var test = function(x, y, z) {
        return x * Math.exp(-(x * x + y * y + z * z));
    };

    return {
        ScalarField: ScalarField,
        sphere: sphere,
        torus: torus,
        sto: sto,
        test: test
    };
});
