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
          'patch.edgecolor': 'black', 'legend.edgecolor': 'black'}
axis = {'axes.formatter.useoffset': False}
text = {'text.usetex': False, 'font.weight': "normal"}
mathtext = {'mathtext.default': 'rm', 'mathtext.fontset': 'stix'}
save = {'savefig.format': 'pdf', 'savefig.bbox': 'tight',
        'savefig.transparent': True, 'savefig.pad_inches': 0.1,
        'pdf.compression': 9}


def qualitative(name="cubehelix", n=5):
    """
    Perceptually uniform qualitative color palette.

    .. code-block:: Python

        # Alter the global palette
        from exa import mpl
        mpl.reconfigure(palette=mpl.qualitative(n=8))

    Args:
        name (str): Palette name
        n (int): Number of colors
    """
    return sns.color_palette(name, n)


def sequential(name="viridis", n=5, desat=None):
    """
    Perceptually uniform sequential color palette.

    .. code-block:: Python

        # Alter the global palette
        from exa import mpl
        mpl.reconfigure(palette=mpl.sequential(n=5))

    Args:
        name (str): Palette name
        n (int): Number of colors
        desat (float): Color desaturation
    """
    return sns.color_palette(name, n, desat)


def diverging(name="BrBG", n=5, desat=None):
    """
    Colorblind sensitive diverging color palette.

    .. code-block:: Python

        # Alter the global palette
        from exa import mpl
        mpl.reconfigure(palette=mpl.diverging(n=5))

    Args:
        name (str): Palette name
        n (int): Number of colors
        desat (float): Color desaturation
    """
    return sns.color_palette("BrBG", n, desat)


def reconfigure(**kwargs):
    """
    Set the Matplotlib configuration using the module level variables ``legend``,
    ``axis``, ``mathtext``, ``text``, ``save``, and additional kwargs.

    Args:
        kwargs: Keyword arguments to be passed to matplotlib's `rc`_

    Note:
        Additional keyword arguments overrule module defaults.

    .. _rc: http://matplotlib.org/users/customizing.html
    """
    context = kwargs.pop('context', 'poster')
    font_scale = kwargs.pop('font_scale', 1.6)
    font = kwargs.pop('font', 'serif')
    style = kwargs.pop('style', 'white')
    palette = kwargs.pop('palette', qualitative(n=5))
    rc = {}
    rc.update(legend)
    rc.update(axis)
    rc.update(mathtext)
    rc.update(text)
    rc.update(save)
    rc.update(kwargs)    # User kwargs overrule default kwargs
    sns.set(context=context, style=style, palette=palette,
            font_scale=font_scale, font=font, rc=rc)


reconfigure()
