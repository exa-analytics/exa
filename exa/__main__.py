#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Executables
########################
Exa provides two executables; "exa" and "exw". For the graphical user interface,
built on top of the Jupyter notebook environment, run "exa" on the command line.
"""
import platform
import argparse
import subprocess
from exa._config import set_update, config
try:
    from exatomic._config import set_update as exatomic_up
except ImportError:
    def tmp():
        return
    exatomic_up = tmp


def notebook():
    """
    Start the exa notebook gui (a Jupyter notebook environment).
    """
    if platform.system().lower() == 'windows':
        subprocess.Popen(['jupyter', 'notebook'], shell=True, cwd=config['paths']['notebooks'])
    else:
        subprocess.Popen(['jupyter notebook'], shell=True, cwd=config['paths']['notebooks'])


def update():
    """
    Update
    """
    set_update()
    exatomic_up()


def workflow(wkflw):
    """
    Args:
        wkflw: Path to workflow script or instance of workflow class.
    """
    raise NotImplementedError('Workflows are currently unsupported.')


def main():
    """
    Main entry point for the application.
    """
    parser = argparse.ArgumentParser(description="Launcher for exa")
    parser.add_argument(
        '-u',
        '--update',
        action='store_true',
        help='Update static data and extensions and launch Jupyter notebook.'
    )
    parser.add_argument(
        '-w',
        '--workflow',
        type=str,
        help='Workflow not implemented',
        required=False,
        default=None
    )
    args = parser.parse_args()
    if args.update == True:
        update()
    elif args.workflow is not None:
        workflow(args.workflow)
    else:
        notebook()


if __name__ == '__main__':
    main()
