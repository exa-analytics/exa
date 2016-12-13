# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Matplotlib Utilities
###############################
Matplotlib is the defacto plotting standard for Python. It can be used
interactively or in the console (spawning a separate visualization window).
This module provides some smart defaults which appeal to the widest possible
audience and print formats. For convenience, the exa framework uses `seaborn`_
which has been tightly integrated with the `PyData`_ stack to provide attractive
and informative visualizations.

.. _seaborn: https://stanford.edu/~mwaskom/software/seaborn/
.. _PyData: http://pydata.org/
"""
import seaborn as sns


def qualitative(n=5):
    """Perceptually uniform qualitative color palette."""
    return sns.color_palette("cubehelix", n)


def sequential(name="viridis", n=5, desat=None):
    """Perceptually uniform sequential color palette."""
    return sns.color_palette(name, n, desat)


def diverging(name="BrBG", n=5, desat=None):
    """Colorblind sensitive diverging color palette."""
    return sns.color_palette("BrBG", n, desat)


def reconfigure():
    """Set the Matplotlib configuration."""
    legend = {'legend.frameon': True, 'legend.facecolor': 'white',
              'legend.fancybox': True, 'patch.facecolor': 'white',
              'patch.edgecolor': 'black'}
    axis = {'axes.formatter.useoffset': False}
    mathtext = {'mathtext.default': 'rm', 'mathtext.fontset': 'stix'}
    save = {'savefig.bbox': 'tight'}
    rc = legend
    rc.update(axis)
    rc.update(mathtext)
    rc.update(save)
    sns.set(context='poster', style='white', palette=qualitative(),
            font_scale=1.6, font='serif', rc=rc)


reconfigure()
