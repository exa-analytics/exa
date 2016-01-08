#!/usr/bin/env python

import sys
if sys.version_info < (3, 4):
    raise Exception('exa requires Python 3.4+')

from setuptools import setup, find_packages
from exa import __version__

# Setuptools installs via pip
DEPS = ['numpy>=1.10.0',
        'scipy>=0.16',
        'pandas>=0.17',
        'scikit-learn>=0.17',
        'tables>=3.2.2',       # pytables
        'pyyaml>=3.11',
        'jupyter>=1.0.0',
        'notebook>=4.0.6',
        'ipython>=4.0.0',
        'ipywidgets>=4.0.0',
        'matplotlib>=1.5.0',
        'seaborn>=0.6.0',
        'sphinx>=1.3',
        'sphinx_rtd_theme>=0.1.7',
        'sphinxcontrib-autoanysrc',
        'argparse',
        'more_itertools']

try:
    setup(name='exa',
          version=__version__,
          description='Core exa functionality',
          author='Tom Duignan & Alex Marchenko',
          author_email='exa.data.analytics@gmail.com',
          url='https://exa-analytics.github.io/website',
          packages=find_packages(),
          package_data={'exa': ['templates/*', 'static/js/*.js', 'static/js/libs/*'
                                'static/css/*', 'static/img/*']},
          entry_points={'console_scripts': ['exa = exa.__main__:main']},
          include_package_data=True,
          install_requires=DEPS)
finally:
    from exa.install import initialize
    initialize()
