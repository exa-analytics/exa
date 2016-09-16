#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Applications
########################
"""
import platform
import argparse
import subprocess
from exa._config import config, reconfigure


def notebook():
    """
    Start the Jupyter notebook.
    """
    if platform.system().lower() == "windows":
        subprocess.Popen(["jupyter", "notebook"], shell=True, cwd=config["paths"]["notebooks"])
    else:
        subprocess.Popen(["jupyter notebook"], shell=True, cwd=config["paths"]["notebooks"])


def workflow(wkflw):
    """
    Args:
        wkflw: Path to workflow script or instance of workflow class.
    """
    raise NotImplementedError("Workflows are currently unsupported.")


def main():
    """
    Defines the possible arguments for the application.
    """
    parser = argparse.ArgumentParser(description="Launcher for exa")
    parser.add_argument(
        "-up",
        "--update",
        action="store_true",
        help="Update static data and extensions and launch Jupyter notebook.",
        default=False
    )
    parser.add_argument(
        "-nb",
        "--notebook",
        action="store_true",
        help="Starts a Jupyter notebook server in the exa root directory.",
        required=False,
        default=False
    )
    args = parser.parse_args()
    if args.update == True:
        reconfigure()
    if args.notebook == True:
        notebook()


if __name__ == "__main__":
    main()
