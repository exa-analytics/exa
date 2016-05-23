#!/usr/bin/env python
import sys
if sys.version_info < (3, 4):
    raise Exception('exa requires Python 3.4+')
from setuptools import setup, find_packages
from exa import __version__


dependencies = ['sphinxcontrib-autoanysrc', 'xmltodict']


try:
    setup(
        name='exa',
        version=__version__,
        description='Data processing, analysis, and visualization made simple.',
        author='Tom Duignan & Alex Marchenko',
        maintainer_email='exa.data.analytics@gmail.com',
        url='https://exa-analytics.github.io/website',
        packages=find_packages(),
        package_data={'exa': ['static/*.json', 'nbextensions/*.js', 'nbextensions/libs/*.js',
                              'nbextensions/apps/*.js']},
        entry_points={'console_scripts': ['exa = exa.__main__:main']},
        include_package_data=True,
        install_requires=dependencies,
        license='Apache License Version 2.0'
    )
except:
    raise
