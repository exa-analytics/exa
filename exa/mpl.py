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
