/*"""
===============
utility.js
===============
Helper functions used by custom notebook JS.
*/
'use strict';

/*require.config({
    shim: {
    },
});*/

define([], function() {
    var flatten_to_array = function(obj) {
        /*"""
        flatten_to_array
        ==================
        Flattens an array-like object into a 1-D Float32Array object.

        Args:
            obj (object): Array like object to be flattened
        */
        var n = obj.length;
        var m = obj[0].length;
        var flat = new Float32Array(n * m);
        var h = 0;
        for (var i=0; i<n; i++) {
            for (var j=0; j<m; j++) {
                flat[h] = obj[i][j];
                h += 1;
            };
        };
        return flat;
    };

    var create_float_array_xyz = function(x, y, z) {
        /*"""
        create_float_array_xyz
        ==========================
        Create a 1D array from 3D data.
        */
        var nx = x.length || 1;
        var ny = y.length || 1;
        var nz = z.length || 1;
        var n = Math.max(nx, ny, nz);
        if (nx == 1) {
            x = repeat_float(x, n);
        };
        if (ny == 1) {
            y = repeat_float(y, n);
        };
        if (nz == 1) {
            z = repeat_float(z, n);
        };
        var xyz = new Float32Array(n * 3)
        for (var i=0, i3=0; i<n; i++, i3+=3) {
            xyz[i3] = x[i];
            xyz[i3+1] = y[i];
            xyz[i3+2] = z[i];
        };
        return xyz;
    };

    var repeat_float = function(value, n) {
        /*"""
        repeat_float
        ==================
        Repeat a value n times.
        */
        var array = new Float32Array(n);
        for (var i=0; i<n; i++) {
            array[i] = value
        };
        return array;
    };

    var repeat_object = function(value, n) {
        /*"""
        repeat_object
        ==============
        Repeat an object n time.
        */
        var obj = [];
        for (var i=0; i<n; i++) {
            obj.push(value);
        };
        return obj;
    };

    var mapper = function(indices, map) {
        /*"""
        mapper
        --------
        */
        var n = indices.length;
        var mapped = [];
        for (var i=0; i<n; i++) {
            mapped.push(map[indices[i]])
        };
        return mapped;
    };

    return {
        'flatten_to_array': flatten_to_array,
        'create_float_array_xyz': create_float_array_xyz,
        'repeat_float': repeat_float,
        'repeat_object': repeat_object,
        'mapper': mapper,
    };
});
