#<<<<<<< HEAD
## -*- coding: utf-8 -*-
## Copyright (c) 2015-2017, Exa Analytics Development Team
## Distributed under the terms of the Apache License 2.0
#"""
#Matplotlib Utilities
################################
#Matplotlib is the defacto plotting standard for Python. It can be used
#interactively in a Jupyter notebook or in the console (spawning a
#separate visualization window). This module provides some defaults which appeal
#to the widest possible audience and support the largest possible print formats.
#Additionally, some convenient plotting wrappers are provided here. All settings
#can be modified on-the-fly:
#
#.. code-block:: Python
#
#    exa.mpl.legend['legend.fancybox'] = False
#    exa.mpl.reconfigure()
#
#    # Additional styling can be passed
#    exa.mpl.reconfigure("patch.facecolor"="black")
#"""
#import seaborn as sns
#
#
#legend = {'legend.frameon': True, 'legend.facecolor': 'white',
#          'legend.fancybox': True, 'patch.facecolor': 'white',
#          'patch.edgecolor': 'black', 'legend.edgecolor': 'black'}
#axis = {'axes.formatter.useoffset': False}
#text = {'text.usetex': False, 'font.weight': "normal"}
#mathtext = {'mathtext.default': 'rm', 'mathtext.fontset': 'stix'}
#save = {'savefig.format': 'pdf', 'savefig.bbox': 'tight',
#        'savefig.transparent': True, 'savefig.pad_inches': 0.1,
#        'pdf.compression': 9}
#
#
#def qualitative(name="cubehelix", n=5):
#    """
#    Perceptually uniform qualitative color palette.
#
#    .. code-block:: Python
#
#        # Alter the global palette
#        from exa import mpl
#        mpl.reconfigure(palette=mpl.qualitative(n=8))
#
#    Args:
#        name (str): Palette name
#        n (int): Number of colors
#    """
#    return sns.color_palette(name, n)
#
#
#def sequential(name="viridis", n=5, desat=None):
#    """
#    Perceptually uniform sequential color palette.
#
#    .. code-block:: Python
#
#        # Alter the global palette
#        from exa import mpl
#        mpl.reconfigure(palette=mpl.sequential(n=5))
#
#    Args:
#        name (str): Palette name
#        n (int): Number of colors
#        desat (float): Color desaturation
#    """
#    return sns.color_palette(name, n, desat)
#
#
#def diverging(name="BrBG", n=5, desat=None):
#    """
#    Colorblind sensitive diverging color palette.
#
#    .. code-block:: Python
#
#        # Alter the global palette
#        from exa import mpl
#        mpl.reconfigure(palette=mpl.diverging(n=5))
#
#    Args:
#        name (str): Palette name
#        n (int): Number of colors
#        desat (float): Color desaturation
#    """
#    return sns.color_palette("BrBG", n, desat)
#
#
#def reconfigure(**kwargs):
#    """
#    Set the Matplotlib configuration using the module level variables ``legend``,
#    ``axis``, ``mathtext``, ``text``, ``save``, and additional kwargs.
#
#    Args:
#        kwargs: Keyword arguments to be passed to matplotlib's `rc`_
#
#    Note:
#        Additional keyword arguments overrule module defaults.
#
#    .. _rc: http://matplotlib.org/users/customizing.html
#    """
#    context = kwargs.pop('context', 'poster')
#    font_scale = kwargs.pop('font_scale', 1.6)
#    font = kwargs.pop('font', 'serif')
#    style = kwargs.pop('style', 'white')
#    palette = kwargs.pop('palette', qualitative(n=5))
#    rc = {}
#    rc.update(legend)
#    rc.update(axis)
#    rc.update(mathtext)
#    rc.update(text)
#    rc.update(save)
#    rc.update(kwargs)    # User kwargs overrule default kwargs
#    sns.set(context=context, style=style, palette=palette,
#            font_scale=font_scale, font=font, rc=rc)
#
#
#reconfigure()
#=======
## -*- coding: utf-8 -*-
## Copyright (c) 2015-2017, Exa Analytics Development Team
## Distributed under the terms of the Apache License 2.0
#"""
#Matplotlib Utilities
################################
#"""
#import seaborn as sns
#import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
#
#
#legend = {'legend.frameon': True, 'legend.facecolor': 'white',
#          'legend.fancybox': True, 'patch.facecolor': 'white',
#          'patch.edgecolor': 'black'}
#axis = {'axes.formatter.useoffset': False}
#mpl_legend = {'legend.frameon': True, 'legend.facecolor': 'white',
#           'legend.edgecolor': 'black'}
#mpl_mathtext = {'mathtext.default': 'rm'}
#mpl_save = {'savefig.format': 'pdf', 'savefig.bbox': 'tight',
#         'savefig.transparent': True, 'savefig.pad_inches': 0.1,
#         'pdf.compression': 9}
#mpl_rc = mpl_legend
#mpl_rc.update(mpl_mathtext)
#mpl_rc.update(mpl_save)
#sns.set(context='poster', style='white', palette='colorblind', font_scale=1.3,
#        font='serif', rc=mpl_rc)
#
#
#def _gen_projected(nxplot, nyplot, projection, figargs):
#    total = nxplot * nyplot
#    fig = sns.mpl.pyplot.figure(**figargs)
#    kwargs = {'projection': projection}
#    axs = [fig.add_subplot(nxplot, nyplot, i, **kwargs) for i in range(1, total + 1)]
#    return fig, axs
#
#
#def _gen_shared(nxplot, nyplot, sharex, sharey, figargs):
#    fig, axs = sns.mpl.pyplot.subplots(nxplot, nyplot, sharex=sharex,
#                                       sharey=sharey, **figargs)
#    axs = fig.get_axes()
#    return fig, axs
#
#
#def _gen_figure(nxplot=1, nyplot=1, figargs=None, projection=None,
#                sharex='none', joinx=False, sharey='none', joiny=False,
#                x=None, nxlabel=None, xlabels=None, nxdecimal=None, xmin=None, xmax=None,
#                y=None, nylabel=None, ylabels=None, nydecimal=None, ymin=None, ymax=None,
#                z=None, nzlabel=None, zlabels=None, nzdecimal=None, zmin=None, zmax=None,
#                r=None, nrlabel=None, rlabels=None, nrdecimal=None, rmin=None, rmax=None,
#                t=None, ntlabel=None, tlabels=None, fontsize=20):
#    """
#    Returns a figure object with as much customization as provided.
#    """
#    figargs = {} if figargs is None else figargs
#    if projection is not None:
#        fig, axs = _gen_projected(nxplot, nyplot, projection, figargs)
#    else:
#        fig, axs = _gen_shared(nxplot, nyplot, sharex, sharey, figargs)
#    adj = {}
#    if joinx: adj.update({'hspace': 0})
#    if joiny: adj.update({'wspace': 0})
#    fig.subplots_adjust(**adj)
#    data = {}
#    if projection is None:
#        data = {'x': x, 'y': y}
#    elif projection == '3d':
#        data = {'x': x, 'y': y, 'z': z}
#    elif projection == 'polar':
#        data = {'r': r, 't': t}
#    methods = {}
#    for ax in axs:
#        if 'x' in data:
#            methods['x'] = (ax.set_xlim, ax.set_xticks, ax.set_xticklabels,
#                            nxlabel, xlabels, nxdecimal, xmin, xmax)
#        if 'y' in data:
#            methods['y'] = (ax.set_ylim, ax.set_yticks, ax.set_yticklabels,
#                            nylabel, ylabels, nydecimal, ymin, ymax)
#        if 'z' in data:
#            methods['z'] = (ax.set_zlim, ax.set_zticks, ax.set_zticklabels,
#                            nzlabel, zlabels, nzdecimal, zmin, zmax)
#        if 'r' in data:
#            methods['r'] = (ax.set_rlim, ax.set_rticks, ax.set_rgrids,
#                            nrlabel, rlabels, nrdecimal, rmin, rmax)
#        if 't' in data:
#            methods['t'] = (ax.set_thetagrids, ntlabel, tlabels)
#        for dim, arr in data.items():
#            if dim == 't':
#                grids, nlabel, labls = methods[dim]
#                if ntlabel is not None:
#                    theta = np.arange(0, 2 * np.pi, 2 * np.pi / ntlabel)
#                    if labls is not None:
#                        grids(np.degrees(theta), labls, fontsize=fontsize)
#                    else:
#                        grids(np.degrees(theta), fontsize=fontsize)
#            else:
#                lim, ticks, labels, nlabel, labls, decs, mins, maxs = methods[dim]
#                if arr is not None:
#                    amin = mins if mins is not None else arr.min()
#                    amax = maxs if maxs is not None else arr.max()
#                    lim((amin, amax))
#                elif mins is not None and maxs is not None:
#                    if nlabel is not None:
#                        ticks(np.linspace(amin, amax, nlabel))
#                        if decs is not None:
#                            sub = "{{:.{}f}}".format(decs).format
#                            labels([sub(i) for i in np.linspace(amin, amax, nlabel)])
#                if labls is not None:
#                    labels(labls)
#                ax.tick_params(axis=dim, labelsize=fontsize)
#    return fig
#
#
#def _plot_surface(x, y, z, nxlabel, nylabel, nzlabel, method,
#                  figargs, axargs):
#    fig = _gen_figure(x=x, y=y, z=z, nxlabel=nxlabel,
#                      nylabel=nylabel, nzlabel=nzlabel,
#                      figargs=figargs, projection='3d')
#    ax = fig.get_axes()[0]
#    convenience = {'wireframe': ax.plot_wireframe,
#                     'contour': ax.contour,
#                    'contourf': ax.contourf,
#                     'trisurf': ax.plot_trisurf,
#                     'scatter': ax.scatter,
#                        'line': ax.plot}
#    if method not in convenience.keys():
#        raise Exception('Method must be in {}.'.format(convenience.keys()))
#    sx, sy = np.meshgrid(x, y)
#    if method in ['trisurf', 'scatter', 'line']:
#        if method == 'line':
#            axargs = {key: val for key, val in axargs.items() if key != 'cmap'}
#        convenience[method](sx.flatten(), sy.flatten(), z.flatten(), **axargs)
#    else:
#        convenience[method](sx, sy, z, **axargs)
#    return fig
#
#
#def _plot_contour(x, y, z, vmin, vmax, cbarlabel, ncbarlabel, ncbardecimal,
#                  nxlabel, nylabel, method, colorbar, figargs, axargs):
#    fig = _gen_figure(x=x, y=y, nxlabel=nxlabel, nylabel=nylabel, figargs=figargs)
#    ax = fig.get_axes()[0]
#    convenience = {'contour': ax.contour,
#                  'contourf': ax.contourf,
#                'pcolormesh': ax.pcolormesh,
#                    'pcolor': ax.pcolor}
#    if method not in convenience.keys():
#        raise Exception('method must be in {}'.format(convenience.keys()))
#    t = convenience[method](x, y, z, **axargs)
#    cbar = fig.colorbar(t) if colorbar else None
#    if cbar is not None and cbarlabel is not None:
#        cbar.set_label(cbarlabel)
#    if cbar is not None and ncbarlabel is not None:
#        newticks = np.linspace(vmin, vmax, ncbarlabel)
#        cbar.set_ticks(newticks)
#        if ncbardecimal is not None:
#            fmt = '{{:.{}f}}'.format(ncbardecimal).format
#            cbar.set_ticklabels([fmt(i) for i in newticks])
#    return fig, cbar
#>>>>>>> 0.3.9
