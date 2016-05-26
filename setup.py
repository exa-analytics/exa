#!/usr/bin/env python
import sys
if sys.version_info < (3, 4):
    raise Exception('exa requires Python 3.4+')
from setuptools import setup, find_packages
from exa import __version__


dependencies = ['sphinxcontrib-autoanysrc', 'xmltodict']


setup(
    name='exa',
    version=__version__,
    description='Data industry specific, processing, analysis, and visualization',
    author='Tom Duignan, Alex Marchenko',
    author_email='exa.data.analytics@gmail.com',
    maintainer_email='exa.data.analytics@gmail.com',
    url='https://exa-analytics.github.io',
    download_url = 'https://github.com/exa-analytics/exa/tarball/v{}'.format(__version__),
    packages=find_packages(),
    package_data={'exa': ['_static/*.json', '_nbextensions/*.js',
                          '_nbextensions/libs/*.js', '_nbextensions/apps/*.js']},
    entry_points={'console_scripts': ['exa = exa.__main__:main']},
    include_package_data=True,
    install_requires=dependencies,
    license='Apache License Version 2.0'
)
