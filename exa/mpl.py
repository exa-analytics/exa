# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Matplotlib Utilities
###############################
Matplotlib is the defacto plotting standard for Python. It can be used
interactively in a Jupyter notebook or in the console (spawning a
separate visualization window). This module provides some defaults which appeal
to the widest possible audience and support the largest possible print formats.
Additionally, some convenient plotting wrappers are provided here. All settings
can be modified on-the-fly:

.. code-block:: Python

    exa.mpl.legend['legend.fancybox'] = False
    exa.mpl.reconfigure()

    # Additional styling can be passed
    exa.mpl.reconfigure("patch.facecolor"="black")
"""
import seaborn as sns


legend = {'legend.frameon': True, 'legend.facecolor': 'white',
          'legend.fancybox': True, 'patch.facecolor': 'white',
          'patch.edgecolor': 'black'}
axis = {'axes.formatter.useoffset': False}
mathtext = {'mathtext.default': 'rm', 'mathtext.fontset': 'stix'}
save = {'savefig.bbox': 'tight'}


def qualitative(n=5):
    """
    Perceptually uniform qualitative color palette.

    To set the palette do:

    .. code-block:: Python

        n = 8
        exa.mpl.reconfigure(palette=exa.mpl.qualitative(n))
    """
    return sns.color_palette("cubehelix", n)


def sequential(name="viridis", n=5, desat=None):
    """
    Perceptually uniform sequential color palette.

    To set the palette do:

    .. code-block:: Python

        name = 'plasma'
        n = 8
        exa.mpl.reconfigure(palette=exa.mpl.sequential(name=name, n=n))
    """
    return sns.color_palette(name, n, desat)


def diverging(name="BrBG", n=5, desat=None):
    """
    Colorblind sensitive diverging color palette.

    To set the palette do:

    .. code-block:: Python

        n = 8
        exa.mpl.reconfigure(palette=exa.mpl.divirging(n=n))
    """
    return sns.color_palette("BrBG", n, desat)


def reconfigure(**kwargs):
    """Set the Matplotlib configuration."""
    palette = kwargs.pop('palette', qualitative(5))
    rc = legend
    rc.update(axis)
    rc.update(mathtext)
    rc.update(save)
    rc.update(kwargs)    # User kwargs overrule default kwargs
    sns.set(context='poster', style='white', palette=palette,
            font_scale=1.6, font='serif', rc=rc)


reconfigure()
