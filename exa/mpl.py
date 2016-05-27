# -*- coding: utf-8 -*-
'''
Matplotlib Utilities
###############################
'''
import seaborn as sns

mpl_legend = {'legend.frameon': True, 'legend.facecolor': 'white',
           'legend.edgecolor': 'black'}
mpl_mathtext = {'mathtext.default': 'rm'}
mpl_save = {'savefig.format': 'pdf', 'savefig.bbox': 'tight',
         'savefig.transparent': True, 'savefig.pad_inches': 0.1,
         'pdf.compression': 9}
mpl_rc = _legend
mpl_rc.update(_mathtext)
mpl_rc.update(_save)
sns.set(context='poster', style='white', palette='colorblind', font_scale=1.3,
        font='serif', rc=_rc)


def savefig(path, ax, dpi=300, **kwargs):
    '''
    Save figure with sensible defaults.
    '''
    fig = ax.get_figure()
    fig.savefig(path, dpi=300, **kwargs)
