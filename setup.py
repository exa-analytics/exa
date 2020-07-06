#!/usr/bin/env python
import os
from setuptools import setup, find_packages


NAME = "exa"
DESCRIPTION = "A framework for data engineering and science"
STATIC = "static"
README = "README.md"
REQUIREMENTS = "requirements.txt"
try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert_file(README, "rst")
except ImportError:
    with open(README) as f:
        LONG_DESCRIPTION = f.read()
with open(REQUIREMENTS) as f:
    DEPENDENCIES = f.read().splitlines()
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "exa", "static", "version.txt"))) as f:
    __version__ = f.read().strip()


setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    package_data={NAME: [STATIC + "/*"]},
    include_package_data=True,
    install_requires=DEPENDENCIES,
    packages=find_packages(),
    zip_safe=False,
    license="Apache License Version 2.0",
    author="The Exa Analytics development team",
    author_email="exa.data.analytics@gmail.com",
    project_urls={
        "Bug Tracker": "https://github.com/exa-analytics/exa/issues",
        "Documentation": "https://exa-analytics.github.io/exa/",
        "Source Code": "https://github.com/exa-analytics/exa"
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Natural Language :: English"
    ]
)
