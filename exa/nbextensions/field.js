/*"""
===============
field.js
===============
Provides the
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
    class Field {
        /*"""
        Field
        ==============
        Base class for dealing with scalar and vector field data

        Args:
            dimensions: {xmin: xmin, xmax: xmax, dx: dx, ...}

        Note:
            The dimensions argument can alternatively be
            {xvalues: xvalues, yvalues: yvalues, ...} or
            {xmin: xmin, xmax: xmax, nx: nx, ...}
        */
        constructor(dimensions, func_or_values) {
            if (dimensions.hasOwnProperty('xvalues') === true) {
                this.x = dimensions.xvalues;
                this.xmin = Math.min(...dimensions.xvalues);
                this.xmax = Math.max(...dimensions.xvalues);
                this.nx = dimensions.xvalues.length;
            } else if (dimensions.nx !== undefined) {
                this.xmin = dimensions.xmin;
                this.xmax = dimensions.xmax;
                this.nx = dimensions.nx;
                this.x = num.linspace(this.xmin, this.xmax, this.nx);
                this.dx = this.x[1] - this.x[0];
            } else {
                this.xmin = dimensions.xmin;
                this.xmax = dimensions.xmax;
                this.dx = dimensions.dx;
                this.x = num.arange(this.xmin, this.xmax, this.dx);
                this.nx = this.x.length;
            };
            if (dimensions.hasOwnProperty('yvalues') === true) {
                this.y = dimensions.yvalues;
                this.ymin = Math.min(...dimensions.yvalues);
                this.ymax = Math.max(...dimensions.yvalues);
                this.ny = dimensions.yvalues.length;
            } else if (dimensions.ny !== undefined) {
                this.ymin = dimensions.ymin;
                this.ymax = dimensions.ymax;
                this.ny = dimensions.ny;
                this.y = num.linspace(this.ymin, this.ymax, this.ny);
                this.dy = this.y[1] - this.y[0];
            } else {
                this.ymin = dimensions.ymin;
                this.ymax = dimensions.ymax;
                this.dy = dimensions.dy;
                this.y = num.arange(this.ymin, this.ymax, this.dy);
                this.ny = this.y.length;
            };
            if (dimensions.hasOwnProperty('zvalues') === true) {
                this.z = dimensions.zvalues;
                this.zmin = Math.min(...dimensions.zvalues);
                this.zmax = Math.max(...dimensions.zvalues);
                this.nz = dimensions.zvalues.length;
            } else if (dimensions.nz !== undefined) {
                this.zmin = dimensions.zmin;
                this.zmax = dimensions.zmax;
                this.nz = dimensions.nz;
                this.z = num.linspace(this.zmin, this.zmax, this.nz);
                this.dz = this.z[1] - this.z[0];
            } else {
                this.zmin = dimensions.zmin;
                this.zmax = dimensions.zmax;
                this.dz = dimensions.dz;
                this.z = num.arange(this.zmin, this.zmax, this.dz);
                this.nz = this.z.length;
            };
            this.n = this.nx * this.ny * this.nz;
            if (typeof func_or_values === 'function') {
                this.func = func_or_values;
                if (!this.hasOwnProperty('values')) {
                    this.compute_field();
                };
            } else {
                this.values = new Float32Array(func_or_values);
            };
            console.log(Math.min(...this.values));
            console.log(Math.max(...this.values));
        };

        compute_field() {
            /*"""
            compute_field
            --------------
            */
            this.values = new Float32Array(this.n);
            var i = 0;
            for (let x of this.x) {
                for (let y of this.y) {
                    for (let z of this.z) {
                        this.values[i] = this.func(x, y, z);
                        ++i;
                    };
                };
            };
        };
    };

    class ScalarField extends Field {
        constructor(dimensions, func_or_values) {
            /*"""
            ScalarField
            =============
            Representation of a scalar field.
            */
            super(dimensions, func_or_values);
        };
    };

    return {
        Field: Field,
        ScalarField: ScalarField
    };
});
