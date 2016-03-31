/*"""
===============
volume.js
===============
Functions for creating discrete volume data (3D spatial data) from analytical
functions.
*/
'use strict';


define([], function() {
    var make_scalar_field = function(nx, ny, nz, ox, oy, oz, xi, xj, xk,
                                     yi, yj, yk, zi, zj, zk, func) {
        /*"""
        make_scalar_field
        --------------------
        Args:
            nx (int): Discretization in x
            ny (int): Discretization in x
            nz (int): Discretization in x
            ox (float): Origin in x
            oy (float): Origin in y
            oz (float): Origin in z
            xi (float): First component of x
            xj (float): Second component of x
            xk (float): Third component of x
            yi (float): First component of y
            yj (float): Second component of y
            yk (float): Third component of y
            func (function): Function of 3D space (x, y, z) of the shape to make

        Returns:
            cube (array)
        */
        console.log('making volume');
        
    };

    return {'make_scalar_field': make_scalar_field};
});
