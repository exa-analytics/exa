/*"""
===============
num.js
===============
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
        return array;
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
        return array;
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
            b = 0.5;
        };
        if (c === undefined) {
            c = 5.0;
        };
        return (x * x) / (a * a) + (y * y) / (b * b) + (z * z) / (c * c)
    };

    var sphere = function(x, y, z) {
        /*"""
        sphere
        ================
        */
        return x * x + y * y + z * z
    }

    var torus = function(x, y, z, c) {
        if (c === undefined) {
            c = 1.0;
        };
        return Math.pow(c - Math.sqrt(x * x + y * y), 2) + z * z;
    };

    return {
        'linspace': linspace,
        'arange': arange,
        'sphere': sphere,
        'ellipsoid': ellipsoid,
        'torus': torus,
        'function_list_3d': ['sphere', 'torus', 'ellipsoid'],
    };
});
