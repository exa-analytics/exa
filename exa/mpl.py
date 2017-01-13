# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Matplotlib Utilities
###############################
"""
import seaborn as sns
# Subclassing matplotlib Figure and Axes
#from matplotlib.figure import Figure
#from matplotlib.axes import Axes, subplot_class_factory
#from matplotlib.backends.backend_agg import FigureCanvasAgg

import numpy as np
from mpl_toolkits.mplot3d import Axes3D

legend = {'legend.frameon': True, 'legend.facecolor': 'white',
          'legend.fancybox': True, 'patch.facecolor': 'white',
          'patch.edgecolor': 'black'}
axis = {'axes.formatter.useoffset': False}
mpl_legend = {'legend.frameon': True, 'legend.facecolor': 'white',
           'legend.edgecolor': 'black'}
mpl_mathtext = {'mathtext.default': 'rm'}
mpl_save = {'savefig.format': 'pdf', 'savefig.bbox': 'tight',
         'savefig.transparent': True, 'savefig.pad_inches': 0.1,
         'pdf.compression': 9}
mpl_rc = mpl_legend
mpl_rc.update(mpl_mathtext)
mpl_rc.update(mpl_save)
sns.set(context='poster', style='white', palette='colorblind', font_scale=1.3,
        font='serif', rc=mpl_rc)

#def _stale_figure_callback(cls, val):
#    if cls.figure:
#        cls.figure.stale = val
#
#class ExaFigure(Figure):
#    """A custom figure class that allows using custom Axes subclasses."""
#
#    def add_subplot(self, axis, *args, **kwargs):
#        """Override add_subplot to accept custom Axes objects."""
#        key = self._make_key(*args, **kwargs)
#        a = subplot_class_factory(axis)(self, *args, **kwargs)
#        self._axstack.add(key, a)
#        self.sca(a)
#        self.stale = True
#        a._remove_method = self._Figure__remove_ax
#        a.stale_callback = _stale_figure_callback
#        return a
#
#    def __init__(self, *args, **kwargs):
#        super(ExaFigure, self).__init__(*args, **kwargs)
#        print('Must fig.set_canvas(matplotlib.backends.'
#              'backend_agg.FigureCanvasAgg(self))')
#        self.set_canvas(FigureCanvasAgg(self))

#class ExAxes(Axes):
#    """
#    A custom matplotlib Axes object for convenience methods related to
#    various dataframes.
#
#    .. code-block:: Python
#
#        fig = ExaFigure()
#        ax = fig.add_subplot(ExAxes, 111)
#        ax.plot(x, y)
#    """
#    def __init__(self, *args, **kwargs):
#        super(ExAxes, self).__init__(*args, **kwargs)


def _gen_figure(nxplot=1, nyplot=1, joinx=False, joiny=False,
                x=None, y=None, z=None, nxlabel=None, nylabel=None,
                nzlabel=None, figargs=None, projection=None):
    """
    Returns a figure object with as much customization as provided.
    """
    figargs = {} if figargs is None else figargs
    if projection == '3d':
        fig = sns.mpl.pyplot.figure(**figargs)
        axs = fig.add_subplot(111, projection=projection)
    else:
        fig, axs = sns.mpl.pyplot.subplots(nyplot, nxplot, **figargs)
        if joinx:
            fig.subplots_adjust(wspace=0)
        if joiny:
            fig.subplots_adjust(hspace=0)
    # In case axs is returned not as an iterable
    axs = fig.get_axes()
    data = {'x': x, 'y': y}
    methods = {'x': (axs[0].set_xlim, axs[0].set_xticks, nxlabel),
               'y': (axs[0].set_ylim, axs[0].set_yticks, nylabel)}
    if projection == '3d':
        data['z'] = z
        methods['z'] = (axs[0].set_zlim, axs[0].set_zticks, nzlabel)
    for cart, arr in data.items():
        lim, ticks, nlabel = methods[cart]
        if arr is not None:
            lim((arr.min(), arr.max()))
            if nlabel is not None:
                ticks(np.linspace(arr.min(), arr.max(), nlabel))
    return fig


def _plot_surface(x, y, z, nxlabel, nylabel, nzlabel, method, figargs, axargs):
    fig = _gen_figure(x=x, y=y, z=z, nxlabel=nxlabel, nylabel=nylabel, method=method,
                      nzlabel=nzlabel, figargs=figargs, axargs=axargs, projection='3d')
    axs = fig.get_axes()
    convenience = {'wireframe': ax.plot_wireframe,
                    'contourf': ax.contourf,
                     'contour': ax.contour,
                     'trisurf': ax.plot_trisurf,
                     'scatter': ax.scatter,
                        'line': ax.plot}
    if method not in convenience.keys():
        raise Exception('method must be in {}'.format(convenience.keys()))
    sx, sy = np.meshgrid(x, y)
    if method in ['trisurf', 'scatter', 'line']:
        if method == 'line':
            axargs = {key: val for key, val in axargs.items() if key != 'cmap'}
        convenience[method](sx.flatten(), sy.flatten(), z.flatten(), **axargs)
    else:
        convenience[method](sx, sy, z, **axargs)
    return fig

def _plot_contour(x, y, z, nxlabel, nylabel, method, colorbar, figargs, axargs):
    fig = _gen_figure(x=x, y=y, nxlabel=nxl, nylabel=nyl, figargs=figargs)
    axs = fig.get_axes()
    convenience = {'contour': axs[0].contour,
                  'contourf': axs[0].contourf,
                'pcolormesh': axs[0].pcolormesh,
                    'pcolor': ax.pcolor}
    if method not in convenience.keys():
        raise Exception('method must be in {}'.format(convenience.keys()))
    t = convenience[method](x, y, z, **axargs)
    cbar = fig.colorbar(t) if colorbar else None
    return fig, cbar
