#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from exa._version import __version__


NAME = "exa"
DESCRIPTION = "A framework for data engineering and science"
staticdir = "static"
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
with open("version.txt") as f:
    version = f.read().replace("v", "")
with open(os.path.join("exa", "_version.py"), "w") as f:
    f.write(f"__version__ = \"{version}\"")


setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    package_data={NAME: [staticdir + "/*"]},
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
