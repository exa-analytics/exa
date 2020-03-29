#!/usr/bin/env python
from setuptools import setup, find_packages
import versioneer


NAME = "exa"
DESCRIPTION = "A framework for data engineering and science"
staticdir = "static"
README = "README.md"
REQUIREMENTS = "REQUIREMENTS.txt"
try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert(README, "rst")
except ImportError:
    with open(README) as f:
        LONG_DESCRIPTION = f.read()
with open(REQUIREMENTS) as f:
    DEPENDENCIES = f.read().splitlines()


setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    package_data={NAME: [staticdir + "/*"]},
    include_package_data=True,
    install_requires=DEPENDENCIES,
    packages=find_packages(),
    zip_safe=False,
    license="Apache License Version 2.0",
    author="The Exa Analytics development team",
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
