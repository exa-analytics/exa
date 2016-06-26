# -*- coding: utf-8 -*-
'''
Python Plotting Utilities
==========================
'''
import seaborn as sns

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


def savefig(path, ax, dpi=300, **kwargs):
    '''
    Save figure with sensible defaults.
    '''
    fig = ax.get_figure()
    fig.savefig(path, dpi=300, **kwargs)
