/*"""
===============
num.js
===============
Numerical utilities
*/
'use strict';


define([], function() {
    var fac2 = function(number) {
        /*"""
        fac2
        ============
        */
    };

    var hstack = function(arrays) {
        /*"""
        hstack
        ===========
        Horizontally concatenate a list of arrays.
        */
        console.log('NotImplementedError')
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
        return 0.5 * (x * x + y * y + z * z)
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

    var None = function(x, y, z) {
        return 0
    };

    return {
        meshgrid3d: meshgrid3d,
        linspace: linspace,
        arange: arange,
        sphere: sphere,
        ellipsoid: ellipsoid,
        torus: torus,
        None: None,
        function_list_3d: ['None', 'sphere', 'torus', 'ellipsoid'],
    };
});
