#!/usr/bin/env python
import sys
if sys.version_info < (3, 4):
    raise Exception('exa requires Python 3.4+')
from setuptools import setup, find_packages
from exa import __version__

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except:
    with open('README.md') as f:
        description = f.read()
with open('requirements.txt') as f:
    dependencies = f.readlines()

setup(
    name='exa',
    version=__version__,
    description=description,
    author='Tom Duignan, Alex Marchenko',
    author_email='exa.data.analytics@gmail.com',
    maintainer_email='exa.data.analytics@gmail.com',
    url='https://exa-analytics.github.io',
    download_url = 'https://github.com/exa-analytics/exa/tarball/v{}'.format(__version__),
    packages=find_packages(),
    package_data={'exa': ['_static/*.json', '_nbextensions/*.js', '_nbextensions/libs/*.js']},
    entry_points={'console_scripts': ['exa = exa.__main__:notebook',
                                      'exw = exa.__main__:workflow']},
    include_package_data=True,
    install_requires=dependencies,
    license='Apache License Version 2.0'
)
import exa
exa._config.config['db']['update'] = '1'
