#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
import os
from setuptools import setup, find_packages


name = "exa"
description = "The exa framework for data processing, analytics, and visualization."
root = os.path.dirname(os.path.abspath(__file__))
try:
    import pypandoc
    long_description = pypandoc.convert("README.md", "rst")
except ImportError:
    with open("README.md") as f:
        long_description = f.read()
with open("requirements.txt") as f:
    dependencies = f.read().splitlines()
with open(os.path.join(root, name, "_version.py")) as f:
    v = f.readlines()[-2]
    v = v.split('=')[1].strip()[1:-1]
    version = '.'.join(v.replace(" ", "").split(","))
setup_args = {
    "name": name,
    "version": version,
    "description": description,
    "long_description": long_description,
    "package_data": {name: ["static/*"]},
    "include_package_data": True,
    "install_requires": dependencies,
    "packages": find_packages(),
    "license": "Apache License Version 2.0",
    "author": "Thomas J. Duignan and Alex Marchenko",
    "author_email": "exa.data.analytics@gmail.com",
    "maintainer_email": "exa.data.analytics@gmail.com",
    "url": "https://exa-analytics.github.io/" + name,
    "download_url": "https://github.com/exa-analytics/{}/tarball/{}.tar.gz".format(name, version),
    "keywords": ["visualization", "analytics", "framework", "data"],
    "classifiers": [
        "Development Status :: 3 - Alpha",
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
