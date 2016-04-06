#!/usr/bin/env python
import sys
if sys.version_info < (3, 4):
    raise Exception('exa requires Python 3.4+')
from setuptools import setup, find_packages
from exa import __version__

dependencies = [
    'numpy>=1.10.0',
    'scipy>=0.17',
    'pandas>=0.17',
    'sqlalchemy>=1.0.0',
    'scikit-learn>=0.17',
    'networkx>=1.10',
    'jupyter>=1.0.0',
    'notebook>=4.1.0',
    'ipython>=4.1.0',
    'ipywidgets>=4.1.0',
    'matplotlib>=1.5.0',
    'seaborn>=0.7.0',
    'sphinx>=1.3',
    'sphinx_rtd_theme>=0.1.7',
    'sphinxcontrib-autoanysrc',
    'xmltodict>=0.9.0'
]

try:
    setup(
        name='exa',
        version=__version__,
        description='Data processing, analysis, and visualization made simple.',
        author='Tom Duignan & Alex Marchenko',
        maintainer_email='exa.data.analytics@gmail.com',
        url='https://exa-analytics.github.io/website',
        packages=find_packages(),
        package_data={'exa': ['static/*.json', 'nbextensions/*.js', 'nbextensions/lib/*.js',
                              'nbextensions/apps/*.js']},
        entry_points={'console_scripts': ['exa = exa.__main__:main']},
        include_package_data=True,
        install_requires=dependencies,
        license='Apache License Version 2.0'
    )
    from exa._install import install
    install(persistent=True)
except:
    raise
