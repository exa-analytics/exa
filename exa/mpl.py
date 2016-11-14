# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Matplotlib Utilities
###############################
"""
import seaborn as sns
# Subclassing matplotlib Figure and Axes
from matplotlib.figure import Figure
from matplotlib.axes import Axes, subplot_class_factory
#from matplotlib.backends.backend_agg import FigureCanvasAgg

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

def _stale_figure_callback(cls, val):
    if cls.figure:
        cls.figure.stale = val

class ExaFigure(Figure):
    """A custom figure class that allows using custom Axes subclasses."""

    def add_subplot(self, axis, *args, **kwargs):
        """Override add_subplot to accept custom Axes objects."""
        key = self._make_key(*args, **kwargs)
        a = subplot_class_factory(axis)(self, *args, **kwargs)
        self._axstack.add(key, a)
        self.sca(a)
        self.stale = True
        a._remove_method = self._Figure__remove_ax
        a.stale_callback = _stale_figure_callback
        return a

    def __init__(self, *args, **kwargs):
        super(ExaFigure, self).__init__(*args, **kwargs)
        print('Must fig.set_canvas(matplotlib.backends.'
              'backend_agg.FigureCanvasAgg(self))')
#        self.set_canvas(FigureCanvasAgg(self))

class ExAxes(Axes):
    """
    A custom matplotlib Axes object for convenience methods related to
    various dataframes.

    .. code-block:: Python

        fig = ExaFigure()
        ax = fig.add_subplot(ExAxes, 111)
        ax.plot(x, y)
    """
    def __init__(self, *args, **kwargs):
        super(ExAxes, self).__init__(*args, **kwargs)
