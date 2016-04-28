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
            this.func = {};
            if (dimensions.hasOwnProperty('x') === true) {
                this.x = dimensions.x;
                this.xmin = Math.min(...this.x);
                this.xmax = Math.max(...this.x);
                this.nx = dimensions.x.length;
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
            if (dimensions.hasOwnProperty('y') === true) {
                this.y = dimensions.y;
                this.ymin = Math.min(...dimensions.y);
                this.ymax = Math.max(...dimensions.y);
                this.ny = dimensions.y.length;
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
            if (dimensions.hasOwnProperty('z') === true) {
                this.z = dimensions.z;
                this.zmin = Math.min(...dimensions.z);
                this.zmax = Math.max(...dimensions.z);
                this.nz = dimensions.z.length;
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
                this.compute_field();
            } else {
                this.values = new Float32Array(func_or_values);
            };
        };

        new_dr(d) {
            /*"""
            new_dr
            -------------
            Updates the y array using the new step size.

            Args:
                d: {dx: dx, ...}
            */
            if (typeof this.func === 'function') {
                var all_equal = 0;
                if (!d.hasOwnProperty('dx')) {
                    d['dx'] = this.dx;
                    ++all_equal;
                } else {
                    this.dx = d.dx;
                    this.x = num.arange(this.xmin, this.xmax, this.dx);
                    this.nx = this.x.length;
                };
                if (!d.hasOwnProperty('dy')) {
                    d['dy'] = this.dy;
                    ++all_equal;
                } else {
                    this.dy = d.dy;
                    this.y = num.arange(this.ymin, this.ymax, this.dy);
                    this.ny = this.y.length;
                };
                if (!d.hasOwnProperty('dz')) {
                    d['dz'] = this.dz;
                    ++all_equal;
                } else {
                    this.dz = d.dz;
                    this.z = num.arange(this.zmin, this.zmax, this.dz);
                    this.nz = this.z.length;
                };
                if (all_equal === 3) {
                    return;
                };
                this.compute_field();
            } else {
                console.log('Cannot automatically update a field with no analytical form!');
            };
        };

        new_limits(limits) {
            /*"""
            new_limits
            --------------
            Args:
                limits: {xmin: xmin, ymin: ymin, ...}
            */
            if (typeof this.func === 'function') {
                var all_equal = 0;
                var x = false;
                var y = false;
                var z = false;
                if (!limits.hasOwnProperty('xmin')) {
                    limits['xmin'] = this.xmin;
                    ++all_equal;
                } else {
                    this.xmin = limits.xmin;
                    x = true;
                };
                if (!limits.hasOwnProperty('ymin')) {
                    limits['ymin'] = this.ymin;
                    ++all_equal;
                } else {
                    this.ymin = limits.ymin;
                    y = true;
                };
                if (!limits.hasOwnProperty('zmin')) {
                    limits['zmin'] = this.zmin;
                    ++all_equal;
                } else {
                    this.zmin = limits.zmin;
                    z = true;
                };
                if (!limits.hasOwnProperty('xmax')) {
                    limits['xmax'] = this.xmax;
                    ++all_equal;
                } else {
                    this.xmax = limits.xmax;
                    x = true;
                };
                if (!limits.hasOwnProperty('ymax')) {
                    limits['ymax'] = this.ymax;
                    ++all_equal;
                } else {
                    this.ymax = limits.ymax;
                    y = true;
                };
                if (!limits.hasOwnProperty('zmax')) {
                    limits['zmax'] = this.zmax;
                    ++all_equal;
                } else {
                    this.zmax = limits.zmax;
                    z = true;
                };
                if (all_equal === 6) {
                    return;
                };
                if (x === true) {
                    this.x = num.arange(this.xmin, this.xmax, this.dx);
                    this.nx = this.x.length;
                };
                if (y === true) {
                    this.y = num.arange(this.ymin, this.ymax, this.dy);
                    this.ny = this.y.length;
                };
                if (z === true) {
                    this.z = num.arange(this.zmin, this.zmax, this.dz);
                    this.nz = this.z.length;
                };
                this.compute_field();
            } else {
                console.log('Cannot automatically update a field with no analytical form!');
            };
        };

        compute_field() {
            /*"""
            compute_field
            --------------
            */
            console.log('computing field...');
            this.values = new Float32Array(this.n);
            var i = 0;
            for (var x of this.x) {
                for (var y of this.y) {
                    for (var z of this.z) {
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
