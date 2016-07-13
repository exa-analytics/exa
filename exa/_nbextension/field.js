// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
===============
field.js
===============
This module provides infrastructure for storing and manipulating 3D fields. By
standardizing how field data is stored, marching cubes (or other surface
computing algorithms) are easier to work with.
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
            dimensions: {'ox': ox, 'nx': nx, 'dxi': dxi, 'dxj': dxj, 'dxk': dxk,
                         'oy': oy, 'ny': ny, 'dyi': dyi, 'dyj': dyj, 'dyk': dyk,
                         'oz': oz, 'nz': nz, 'dzi': dzi, 'dzj': dzj, 'dzk': dzk}

        Note:
            The dimensions argument can alternatively be
            {'x': xarray, 'y': yarray, 'z': zarray}
            if they have already been constructed but in this
            case the arrays should form cubic discrete points
        */
        constructor(dimensions, func_or_values) {
            this.func = {};
            if (dimensions.hasOwnProperty('x') === true) {
                this.x = dimensions.x;
                this.ox = Math.min(...this.x);
                this.fx = Math.max(...this.x);
                this.nx = this.x.length;
                this.dxi = this.x[1] - this.x[0];
                this.dxj = 0;
                this.dxk = 0;
            } else {
                this.ox = dimensions.ox;
                this.nx = dimensions.nx;
                this.dxi = dimensions.dxi;
                this.dxj = dimensions.dxj;
                this.dxk = dimensions.dxk;
                this.x = num.minspace(this.ox, this.dxi, this.nx);
                this.fx = Math.max(...this.x);
            };
            if (dimensions.hasOwnProperty('y') === true) {
                this.y = dimensions.y;
                this.oy = Math.min(...this.y);
                this.fy = Math.max(...this.y);
                this.ny = this.y.length;
                this.dyi = this.y[1] - this.y[0];
                this.dyj = 0;
                this.dyk = 0;
            } else {
                this.oy = dimensions.oy;
                this.ny = dimensions.ny;
                this.dyi = dimensions.dyi;
                this.dyj = dimensions.dyj;
                this.dyk = dimensions.dyk;
                this.y = num.minspace(this.oy, this.dyj, this.ny);
                this.fy = Math.max(...this.y);
            };
            if (dimensions.hasOwnProperty('z') === true) {
                this.z = dimensions.z;
                this.oz = Math.min(...this.z);
                this.fz = Math.max(...this.z);
                this.nz = this.z.length;
                this.dzi = this.z[1] - this.z[0];
                this.dzj = 0;
                this.dzk = 0;
            } else {
                this.oz = dimensions.oz;
                this.nz = dimensions.nz;
                this.dzi = dimensions.dzi;
                this.dzj = dimensions.dzj;
                this.dzk = dimensions.dzk;
                this.z = num.minspace(this.oz, this.dzk, this.nz);
                this.fz = Math.max(...this.z);
            };
            this.n = this.nx * this.ny * this.nz;
            if (typeof func_or_values === 'function') {
                this.func = func_or_values;
                console.log('field constructor before computing field');
                console.log(this);
                this.values = num.compute_field(this.x, this.y, this.z, this.n, this.func)['values'];
                console.log(this.values);
            } else {
                this.values = new Float32Array(func_or_values);
            };
        };

        update() {
            /*"""
            update
            =========
            Updates the field after establishing new x, y, z arrays
            */
            this.nx = this.x.length;
            this.ny = this.y.length;
            this.nz = this.z.length;
            this.ox = Math.min(...this.x);
            this.oy = Math.min(...this.y);
            this.oz = Math.min(...this.z);
            this.fx = Math.max(...this.x);
            this.fy = Math.max(...this.y);
            this.fz = Math.max(...this.z);
            this.values = num.compute_field(this.x, this.y, this.z, this.n, this.func)['values'];
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
