# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Matplotlib Utilities
###############################
"""
import seaborn as sns


def color_palette(name='plasma', n=8):
    """
    """
    return sns.color_palette(name, n)


legend = {'legend.frameon': True, 'legend.facecolor': 'white',
          'legend.fancybox': True, 'patch.facecolor': 'white',
          'patch.edgecolor': 'black'}
axis = {'axes.formatter.useoffset': False}
mpl_legend = {'legend.frameon': True, 'legend.facecolor': 'white',
              'legend.edgecolor': 'black'}
mpl_mathtext = {'mathtext.default': 'rm', 'mathtext.fontset': 'stix'}
mpl_save = {'savefig.bbox': 'tight'}
mpl_rc = mpl_legend
mpl_rc.update(mpl_mathtext)
mpl_rc.update(mpl_save)
sns.set(context='poster', style='white', palette='plasma',
        font_scale=1.6, font='serif', rc=mpl_rc)
