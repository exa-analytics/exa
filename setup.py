#!/usr/bin/env python
import sys
if sys.version_info < (3, 4):
    raise Exception('exa requires Python 3.4+')
from setuptools import setup, find_packages
from exa import __version__


DEPS = [req.strip() for req in open('requirements.txt').readlines()]
DEPS += ['tables>3.2.2']


try:
    setup(
        name='exa',
        version=__version__,
        description='Core exa functionality',
        author='Tom Duignan & Alex Marchenko',
        author_email='exa.data.analytics@gmail.com',
        url='https://exa-analytics.github.io/website',
        packages=find_packages(),
        package_data={
            'exa': [
                'templates/*',
                'static/js/*.js',
                'static/js/libs/*',
                'static/css/*',
                'static/img/*'
            ]
        },
        entry_points={'console_scripts': ['exa = exa.__main__:main']},
        include_package_data=True,
        install_requires=DEPS
    )
finally:
    from exa.install import initialize
    initialize()
