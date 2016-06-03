# -*- coding: utf-8 -*-
'''
Matplotlib Utilities
###############################
'''
import seaborn as sns

legend = {'legend.frameon': True, 'legend.facecolor': 'white',
          'legend.fancybox': True, 'patch.facecolor': 'white',
          'patch.edgecolor': 'black'}
axis = {'axes.formatter.useoffset': False}

rc = legend
rc.update(axis)
#rc = {**legend, **axis}
sns.set(context='poster', style='white', palette='viridis', font_scale=1.7,
        font='serif', rc=rc)
