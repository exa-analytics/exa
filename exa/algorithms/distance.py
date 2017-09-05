# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Distance Computations
#########################################
This module provides some calculations of distances between objects with support
for both free boundary and periodic boundary conditions.
"""
import numba as nb


@nb.jit(nopython=True, nogil=True, cache=True)
def pdist(x, y, z, index, dmax=1.0):
    """
    Pairwise distances for a collection of objects in 3D space (with free
    boundary conditions).

    Args:
        x (array): Array of x component values (float)
        y (array): Array of y component values (float)
        z (array): Array of z component values (float)
        index (array): Object indices (integer)
        dmax (float): Maximum distance of interest (default 1.0 unit)

    Returns:
        dx (array): Array of distance vector x component
        dy (array): Array of distance vector y component
        dz (array): Array of distance vector z component
        dr (array): Array of distances
        idx (array): Array of indices of first object in pair
        jdx (array): Array of indices of second object in pair
    """
    m = len(x)
    n = m*(m - 1)//2
    # Allocate memory
    dx = np.empty((n, ), dtype=np.float64)
    dx[:] = np.nan
    dy = dx.copy()
    dz = dx.copy()
    dr = dx.copy()
    idx = np.empty((n, ), dtype=np.int64)
    idx[:] = -1
    jdx = idx.copy()
    k = 0
    # For each atom i
    for i in range(m):
        # For each atom j != i
        for j in range(i + 1, m):
            # Compute the (squared) distance vector
            dx_ = (x[i] - x[j])
            dy_ = (y[i] - y[j])
            dz_ = (z[i] - z[j])
            r = dx_**2 + dy_**2 + dz_**2
            # And store it if it is of interest
            if r <= dmax2:
                dx[k] = dx_
                dy[k] = dy_
                dz[k] = dz_
                dr[k] = np.sqrt(r)
                idx[k] = index[i]
                jdx[k] = index[j]
                k += 1
    dx = dx[~np.isnan(dx)]
    dy = dy[~np.isnan(dy)]
    dz = dz[~np.isnan(dz)]
    dr = dr[~np.isnan(dr)]
    idx = idx[idx > -1]
    jdx = jdx[jdx > -1]
    return dx, dy, dz, dr, idx, jdx


@nb.jit(nopython=True, nogil=True)
def pdist_pbc_orthorhomic(ux, uy, uz, a, b, c, index, dmax=1.0, rtol=10**-5, atol=10**-8):
    """
    Pairwise distances for objects in an orthorhombic unit cell with periodic
    boundary conditions.

    An orthorhombic cell is defined by orthogonal vectors of length a and b
    (which define the base) and height vector of length c. All three vectors
    intersect at 90° angles. (For example, if a = b = c the cell is a simple cubic cell.)
    This function assumes the unit cell is constant with respect to an external
    frame of reference and that the origin of the cell is at (0, 0, 0).

    Note:
        By convention each object's projection (from 0 = [-1, -1, -1] to 13 = [0, 0, 0]
        to 26 = [1, 1, 1]) is check in increasing order. The projected position
        returned (see below) is always that of highest projection found that
        has the correct (minimum) distance.

    Args:
        ux (array): Array of unit cell x components
        uy (array): Array of unit cell y components
        uz (array): Array of unit cell z components
        a (float): Unit cell dimension a
        b (float): Unit cell dimension b
        c (float): Unit cell dimension c
        index (array): Object indices (integer)
        dmax (float): Maximum distance of interest
        rtol (float): Relative tolerance (used to check float equivalence)
        atol (float): Absolute tolerance (used to check float equivalence)
    """
    m = [-1, 0, 1]
    dmax2 = dmax**2
    n = len(ux)
    nn = n*(n - 1)//2
    # Allocate memory
    dx = np.empty((nn, ), dtype=np.float64)
    dx[:] = np.nan
    dy = dx.copy()
    dz = dx.copy()
    dr = dx.copy()
    idx = np.empty((nn, ), dtype=np.int64)
    idx[:] = -1
    jdx = idx.copy()
    projection = idx.copy()
    k = 0
    # For each atom i
    for i in range(n):
        xi = ux[i]
        yi = uy[i]
        zi = uz[i]
        # For each atom j
        for j in range(i+1, n):
            xj = ux[j]
            yj = uy[j]
            zj = uz[j]
            dpx = np.nan
            dpy = np.nan
            dpz = np.nan
            dpr = dmax2
            prj = 0
            # Check all projections of atom i's distance to the (in unit cell)
            # position of atom j. Projection indices start at 0 (the -1, -1, -1
            # projection) increasing by the last component to 26 (the 1, 1, 1
            # projection). The 13th projection is the unit cell itself.
            for aa in m:
                for bb in m:
                    for cc in m:
                        pxi = xi + aa*a
                        pyi = yi + bb*b
                        pzi = zi + cc*c
                        dpx_ = pxi - xj
                        dpy_ = pyi - yj
                        dpz_ = pzi - zj
                        dpr_ = dpx_**2 + dpy_**2 + dpz_**2    # Don't unnecessarily compute sqrt
                        # Maximizing the projection index stored is enforced by
                        # the second statement in the or below.
                        if dpr_ <= dpr or np.abs(dpr - dpr_) <= atol + rtol*dpr_:
                            dx[k] = dpx_
                            dy[k] = dpy_
                            dz[k] = dpz_
                            dr[k] = np.sqrt(dpr_)
                            idx[k] = index[i]
                            jdx[k] = index[j]
                            projection[k] = prj
                        prj += 1
            k += 1
    dx = dx[~np.isnan(dx)]
    dy = dy[~np.isnan(dy)]
    dz = dz[~np.isnan(dz)]
    dr = dr[~np.isnan(dr)]
    idx = idx[idx > -1]
    jdx = jdx[jdx > -1]
    projection = projection[projection > -1]
    return dx, dy, dz, dr, idx, jdx, projection
