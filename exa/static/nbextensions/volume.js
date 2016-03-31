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
        var n = nx * ny * nz;
        var field = new Float32Array(n);
        var h = 0;
        var x =
        for (let i=0; i<nx; i++) {
            for (let j=0; j<ny; j++) {
                for (let k=0; k<nz; k++) {
                    field[h] = func()
                };
            };
        };

    };
    return memoize(function() {
  var res = new Array(3);
  for(var i=0; i<3; ++i) {
    res[i] = 2 + Math.ceil((dims[i][1] - dims[i][0]) / dims[i][2]);
  }
  var volume = new Float32Array(res[0] * res[1] * res[2])
    , n = 0;
  for(var k=0, z=dims[2][0]-dims[2][2]; k<res[2]; ++k, z+=dims[2][2])
  for(var j=0, y=dims[1][0]-dims[1][2]; j<res[1]; ++j, y+=dims[1][2])
  for(var i=0, x=dims[0][0]-dims[0][2]; i<res[0]; ++i, x+=dims[0][2], ++n) {
    volume[n] = f(x,y,z);
  }
  return {data: volume, dims:res};
});
}
numeric.linspace = function linspace(a,b,n) {
    if(typeof n === "undefined") n = Math.max(Math.round(b-a)+1,1);
    if(n<2) { return n===1?[a]:[]; }
    var i,ret = Array(n);
    n--;
    for(i=n;i>=0;i--) { ret[i] = (i*b+(n-i)*a)/n; }
    return ret;
}

    return {'make_scalar_field': make_scalar_field};
});
