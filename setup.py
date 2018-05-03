#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from distutils import log
from setuptools import setup, find_packages


name = "exa"
description = "A framework for data science"
staticdir = "static"
readme = "README.md"
requirements = "requirements.txt"
verfile = "_version.py"
root = os.path.dirname(os.path.abspath(__file__))
log.set_verbosity(log.DEBUG)
try:
    import pypandoc
    long_description = pypandoc.convert(readme, "rst")
except ImportError:
    with open(readme) as f:
        long_description = f.read()
with open(requirements) as f:
    dependencies = f.read().splitlines()
with open(os.path.join(root, name, verfile)) as f:
    v = f.readlines()[-2]
    v = v.split('=')[1].strip()[1:-1]
    version = '.'.join(v.replace(" ", "").split(","))


setup_args = {
    'name': name,
    'version': version,
    'description': description,
    'long_description': long_description,
    'package_data': {name: [staticdir + "/*"]},
    'include_package_data': True,
    'install_requires': dependencies,
    'packages': find_packages(),
    'zip_safe': False,
    'license': "Apache License Version 2.0",
    'author': "Thomas J. Duignan, Alex Marchenko, and contributors",
    'author_email': "exa.data.analytics@gmail.com",
    'maintainer_email': "exa.data.analytics@gmail.com",
    'url': "https://exa-analytics.github.io/" + name,
    'download_url': "https://github.com/exa-analytics/{}/archive/v{}.tar.gz".format(name, version),
    'keywords': ["data science", "framework", "jupyter notebook"],
    'classifiers': [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Natural Language :: English"
    ]
}

setup(**setup_args)
