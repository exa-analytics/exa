#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Executable
#############
"""
import argparse
import platform
#
#import os, sys
#HOME = 'J:/Alex'
#sys.path.insert(0, os.sep.join((HOME, 'workspace', 'exa', 'exa')))
#
from subprocess import Popen, PIPE
from exa._config import config


def main():
    parser = argparse.ArgumentParser(description="The exa framework launcher.")
    parser.add_argument(
        "-nb",
        "--notebook",
        action="store_true",
        help="Starts a Jupyter notebook server in the exa notebook directory.",
        required=False,
        default=False
    )
    args = parser.parse_args()
    if args.notebook == True:
        notebook()


def notebook():
    """Start the Jupyter notebook."""
    if platform.system().lower() == "windows":
        proc = Popen(["jupyter", "notebook"], shell=True,
                     cwd=config["paths"]["notebooks"], stdin=PIPE)
    else:
        proc = Popen(["jupyter notebook"], shell=True,
                     cwd=config["paths"]["notebooks"], stdin=PIPE)
    proc.wait()


if __name__ == "__main__":
    main()



#import platform
#import argparse
#import subprocess
#from exa._config import config, reconfigure
#
#
#def workflow(wkflw):
#    """
#    Execute a workflow on given computational resources.
#
#    Args:
#        wkflw: Workflow object
#        resrc: Computational resources
#    """
#    raise NotImplementedError("Workflows are currently unsupported.")
#
#
#def main():
#    """Sets up entry points and help text for executable."""
#    parser = argparse.ArgumentParser(description="Launcher for exa")
#    parser.add_argument(
#        "-up",
#        "--update",
#        action="store_true",
#        help="Update static data and extensions and launch Jupyter notebook.",
#        default=False
#    )
#    parser.add_argument(
#        "-nb",
#        "--notebook",
#        action="store_true",
#        help="Starts a Jupyter notebook server in the exa root directory.",
#        required=False,
#        default=False
#    )
#    args = parser.parse_args()
#    if args.update == True:
#        reconfigure()
#    if args.notebook == True:
#        notebook()
#
#
#
