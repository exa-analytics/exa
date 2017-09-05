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
def nb_pdist(x, y, z, index, dmax=8.0):
    """
    3D free boundary condition
    """
    m = len(x)
    n = m*(m - 1)//2
    dx = np.empty((n, ), dtype=np.float64)
    dx[:] = np.nan
    dy = dx.copy()
    dz = dx.copy()
    dr = dx.copy()
    atom0 = dx.copy()
    atom1 = dx.copy()
    k = 0
    # For each atom i
    for i in range(m):
        # For each other atom j (!= i)
        for j in range(i + 1, m):
            dx_ = (x[i] - x[j])
            dy_ = (y[i] - y[j])
            dz_ = (z[i] - z[j])
            r = dx_**2 + dy_**2 + dz_**2
            if r <= dmax2:
                dx[k] = dx_
                dy[k] = dy_
                dz[k] = dz_
                dr[k] = np.sqrt(r)
                atom0[k] = index[i]
                atom1[k] = index[j]
                k += 1
    dx = dx[~np.isnan(dx)]
    dy = dy[~np.isnan(dy)]
    dz = dz[~np.isnan(dz)]
    dr = dr[~np.isnan(dr)]
    atom0 = atom0[~np.isnan(atom0)]
    atom1 = atom1[~np.isnan(atom1)]
    return dx, dy, dz, dr, atom0, atom1


@nb.jit(nopython=True, nogil=True)
def _pbc_pdist_euc_3d_orthorhombic(ux, uy, uz, a, b, c, index, dmax=1.0, rtol=10**-5, atol=10**-8):
    """
    Pairwise two body calculation for bodies in an orthorhombic periodic cell.

    An orthorhombic cell is defined by orthogonal vectors of length a and b
    (which define the base) and height vector of length c. All three vectors
    intersect at 90° angles. If a = b = c the cell is a simple cubic cell.
    This function assumes the unit cell is constant with respect to an external
    frame of reference and that the origin of the cell is at (0, 0, 0).

    Args:
        ux (array): In unit cell x array
        uy (array): In unit cell y array
        uz (array): In unit cell z array
        a (float): Unit cell dimension a
        b (float): Unit cell dimension b
        c (float): Unit cell dimension c
        index (array): Atom indexes
        dmax (float): Maximum distance of interest
        rtol (float): Relative tolerance (used to check float equivalence)
        atol (float): Absolute tolerance (used to check float equivalence)
    """
    m = [-1, 0, 1]
    dmax2 = dmax**2
    n = len(ux)
    nn = n*(n - 1)//2
    dx = np.empty((nn, ), dtype=np.float64)
    dx[:] = np.nan
    dy = dx.copy()
    dz = dx.copy()
    dr = dx.copy()
    ii = dx.copy()
    jj = dx.copy()
    projection = dx.copy()
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
            # Check all projections of atom i
            # Note that i, j are in the unit cell so we make a 3x3x3 'supercell'
            # of i around j
            # The index of the projections of i go from 0 to 26 (27 projections)
            # The 13th projection is the unit cell itself.
            for aa in m:
                for bb in m:
                    for cc in m:
                        pxi = xi + aa*a
                        pyi = yi + bb*b
                        pzi = zi + cc*c
                        dpx_ = pxi - xj
                        dpy_ = pyi - yj
                        dpz_ = pzi - zj
                        dpr_ = dpx_**2 + dpy_**2 + dpz_**2
                        # The second criteria here enforces that prefer the projection
                        # with the largest value (i.e. 0 = [-1, -1, -1] < 13 = [0, 0, 0] < 26 = [1, 1, 1])
                        # The system sets a fixed preference for the projected positions rather
                        # than having a random choice.
                        if dpr_ <= dpr or np.abs(dpr - dpr_) <= atol + rtol*dpr_:
                            dx[k] = dpx_
                            dy[k] = dpy_
                            dz[k] = dpz_
                            dr[k] = np.sqrt(dpr_)
                            ii[k] = index[i]
                            jj[k] = index[j]
                            projection[k] = prj
                        prj += 1
            k += 1
    dx = dx[~np.isnan(dx)]
    dy = dy[~np.isnan(dy)]
    dz = dz[~np.isnan(dz)]
    dr = dr[~np.isnan(dr)]
    ii = ii[~np.isnan(ii)]
    jj = jj[~np.isnan(jj)]
    projection = projection[~np.isnan(projection)]
    return dx, dy, dz, dr, ii, jj, projection
