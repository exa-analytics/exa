#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
import os, sys
import platform
from distutils import log
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info


name = "exa"
description = "A framework for data processing, computation, and visualization."
datadir = "_data"
nbdir = "_nbextension"
readme = "README.md"
requirements = "requirements.txt"
verfile = "_version.py"
root = os.path.dirname(os.path.abspath(__file__))
is_repo = os.path.exists(os.path.join(here, ".git"))
prckws = {'shell': True} if platform.system().lower() == 'windows' else {}
jsroot = os.path.join(root, "js")
npm_path = os.pathsep.join([os.path.join(jsroot, "node_modules", ".bin"),
                            os.environ.get('PATH', os.defpath)])
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


def update_package_data(distribution):
    """Modify the ``package_data`` to catch changes during setup."""
    build_py = distribution.get_command_obj("build_py")
    build_py.finalize_options()    # Updates package_data


def js_prerelease(command, strict=False):
    """Build minified JS/CSS prior to performing the command."""
    class DecoratedCommand(Command):
        """Used by ``js_prerelease`` to modify JS/CSS prior to running the command."""
        def run(self):
            jsdeps = self.distribution.get_command_obj("jsdeps")
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                command.run(self)
                return
            try:
                self.distribution.run_command("jsdeps")
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn("Rebuilding JS/CSS failed")
                    if missing:
                        log.error("Missing files: {}".format(missing))
                    raise e
                else:
                    log.warn("Rebuilding JS/CSS failed but continuing...")
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)
    return DecoratedCommand


class NPM(Command):
    """Installs package.json dependencies using npm."""
    user_options = []
    node_modules = os.path.join(jsroot, "node_modules")
    targets = [os.path.join(root, name, nbdir, "extension.js"),
               os.path.join(root, name, nbdir, "index.js")]

    def finalize_options(self):
        pass

    def finalize_options(self):
        pass

    def has_npm(self):
        try:
            check_call(["npm", "--version"], **prckws)
            return True
        except Exception:
            return False

    def run(self):
        if not self.has_npm():
            log.error("``npm`` unavailable.")
        else:
            env = os.environ.copy()
            env['PATH'] = npm_path
            log.info("Installing build dependencies with npm...")
            check_call(["npm", "install"], cwd=jsroot, stdout=sys.stdout, stderr=sys.stderr, **prckws)
            os.utime(self.node_modules, None)
        for t in self.targets:
            if not os.path.exists(t):
                msg = "Missing file: {}".format(t)
                if not self.has_npm():
                    msg += r"\n``npm`` is required to build a dev install of {}".format(name)
                raise ValueError(msg)
        update_package_data(self.distribution)


setup_args = {
    'name': name,
    'version': version,
    'description': description,
    'long_description': long_description,
    'zip_safe': False,
    'data_files': [("-".join("share/jupyter/nbextensions/jupyter", name),
                    ["/".join(name, nbdir, "extension.js"),
                     "/".join(name, nbdir, "index.js"),
                     "/".join(name, nbdir, "index.js.map")])],
    'package_data': {name: [datadir + "/*"]},
    'include_package_data': True,
    'install_requires': dependencies,
    'packages': find_packages(),
    'cmdclass': {'build_py': js_prerelease(build_py),
                 'egg_info': js_prerelease(egg_info),
                 'sdist': js_prerelease(sdist, strict=True),
                 'jsdeps': NPM},
    'license': "Apache License Version 2.0",
    'author': "Thomas J. Duignan and Alex Marchenko",
    'author_email': "exa.data.analytics@gmail.com",
    'maintainer_email': "exa.data.analytics@gmail.com",
    'url': "https://exa-analytics.github.io/" + name,
    'download_url': "https://github.com/avmarchenko/{}/tarball/{}.tar.gz".format(name, version),
    'keywords': ["data", "hpc", "visualization", "jupyter", "notebook"],
    'classifiers': [
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
