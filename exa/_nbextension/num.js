// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
=============
num.js
=============
Numerical utilities
*/
'use strict';


define([], function() {

    var hstack = function(arrays) {
        /*"""
        hstack
        ===========
        Horizontally concatenate a list of arrays.
        */
        console.log('NotImplementedError')
    };

    var minspace = function(min, space, n) {
        /*"""
        minspace
        ================
        Creates a linearly spaced array with knowledge of the length,
        origin and spacing of the array.

        Args:
            min (number): origin
            space (number): spacing
            n (number): length of array

        */
        var n1 = n - 1;
        var fol = min;
        var arr = [min];
        for (var i = 0; i < n1; i++) {
            fol += space;
            arr.push(fol);
        };
        return new Float32Array(arr);
    };

    var linspace = function(min, max, n) {
        /*"""
        linspace
        ================
        Create a linearly spaced array of the form [min, max] with n linearly
        spaced elements.

        Args:
            min (number): Starting number
            max (number): Ending number (inclusive)
            n (number): Number of elements

        Returns:
            array (array): Array of values
        */
        var n1 = n - 1;
        var step = (max - min) / n1;
        var array = [min];
        for (var i=0; i<n1; i++) {
            min += step;
            array.push(min);
        };
        return new Float32Array(array);
    };

    var arange = function(min, max, step) {
        /*"""
        arange
        ================
        */
        var array = [min];
        while (min < max) {
            min += step;
            array.push(min);
        };
        return new Float32Array(array);
    };

    var meshgrid3d = function(x, y, z) {
        /*"""
        meshgrid3d
        ============
        From three discrete dimensions, create a set of
        3d gridpoints
        */
        var nx = x.length;
        var ny = y.length;
        var nz = z.length;
        var n = nx * ny * nz;
        var xx = new Float32Array(n);
        var yy = new Float32Array(n);
        var zz = new Float32Array(n);
        var h = 0;
        for (var i of x) {
            for (var j of y) {
                for (var k of z) {
                    xx[h] = i;
                    yy[h] = j;
                    zz[h] = k;
                    h += 1;
                };
            };
        };
        return {x: xx, y: yy, z: zz};
    };

    var ellipsoid = function(x, y, z, a, b, c) {
        /*"""
        ellipsoid
        ===========
        */
        if (a === undefined) {
            a = 2.0;
        };
        if (b === undefined) {
            b = 1.75;
        };
        if (c === undefined) {
            c = 1.5;
        };
        return 2 * ((x * x) / (a * a) + (y * y) / (b * b) + (z * z) / (c * c))
    };

    var sphere = function(x, y, z) {
        /*"""
        sphere
        ================
        */
        return (x * x + y * y + z * z) //* Math.exp( -0.5 * (x * x + y * y + z * z));
    }

    var torus = function(x, y, z, c) {
        /*"""
        torus
        ================
        */
        if (c === undefined) {
            c = 1.0;
        };
        return  Math.pow(c - Math.sqrt(x * x + y * y), 2) + z * z;
    }

    var compute_field = function(xs, ys, zs, n, func) {
        /*"""
        compute_field
        ==============
        */
        var values = new Float32Array(n);
        var norm = 0;
        var dv = (xs[1] - xs[0]) * (ys[1] - ys[0]) * (zs[1] - zs[0]);
        var i = 0;
        for (var x of xs) {
            for (var y of ys) {
                for (var z of zs) {
                    var tmp = func(x, y, z);
                    values[i] = tmp;
                    norm += (tmp * tmp * dv);
                    i += 1;
                };
            };
        };
        norm = 1 / Math.pow(norm, (1/2));
        return {'values': values, 'norm': norm}
    };

    var gen_array = function(nr, or, dx, dy, dz) {
        /*"""
        gen_array
        =============
        Generates discrete spatial points in space. Used to generate
        x, y, z spatial values for the cube field. In most cases, for the x
        basis vector, dy and dz are zero ("cube-like").
        */
        var r = new Float32Array(nr);
        r[0] = or;
        for (var i=1; i<nr; i++) {
            r[i] = r[i-1] + dx + dy + dz;
        };
        return r;
    };

    var normalize_gaussian = function(alpha, L) {
        /*"""
        normalize_gaussian
        ===================
        Given an exponent and a pre-exponential power, return the
        normalization constant of a given gaussian type function.
        */
        var prefac = Math.pow((2 / Math.PI), 0.75);
        var numer = Math.pow(2, L) * Math.pow(alpha, ((L + 1.5) / 2));
        var denom = Math.pow(this.factorial2(2 * L - 1), 0.5);
        return prefac * numer / denom;
    };

    var factorial2 = function(n) {
        /*"""
        factorial2
        ============
        Returns the factorial2 of an integer.
        */
        if (n < -1) {
            return 0;
        } else if (n < 2) {
            return 1;
        } else {
            var prod = 1;
            while (n > 0) {
                prod *= n;
                n -= 2;
            };
            return prod;
        };  
    };


    return {
        meshgrid3d: meshgrid3d,
        linspace: linspace,
        minspace: minspace,
        arange: arange,
        sphere: sphere,
        ellipsoid: ellipsoid,
        torus: torus,
        gen_array: gen_array,
        compute_field: compute_field,
        factorial2: factorial2,
        normalize_gaussian: normaliz_gaussian,
        function_list_3d: [null, 'sphere', 'torus', 'ellipsoid'],
    };
});
