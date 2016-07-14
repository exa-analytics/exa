#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
import sys
if sys.version_info < (3, 4):
    raise Exception('exa requires Python 3.4+')
from setuptools import setup, find_packages
from exa import __version__

with open('README.rst') as f:
    description = f.read()
with open('requirements.txt') as f:
    dependencies = f.readlines()

setup(
    name='exa',
    version=__version__ + 'a',
    description='An ecosystem for data processing, analytics, and visualization.',
    long_description=description,
    author='Tom Duignan, Alex Marchenko',
    author_email='exa.data.analytics@gmail.com',
    maintainer_email='exa.data.analytics@gmail.com',
    url='https://exa-analytics.github.io',
    download_url = 'https://github.com/exa-analytics/exa/tarball/v{}'.format(__version__),
    packages=find_packages(),
    package_data={'exa': ['_static/*.json', '_nbextension/*.js', '_nbextensions/lib/*.js']},
    entry_points={'console_scripts': ['exa = exa.__main__:main']},
    include_package_data=True,
    install_requires=dependencies,
    license='Apache License Version 2.0',
    keywords='analytics visualization big data',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: IPython',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering'
    ]
)
