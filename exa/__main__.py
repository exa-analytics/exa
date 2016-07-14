#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Executables
########################
Exa provides two executables; "exa" and "exw". For the graphical user interface,
built on top of the Jupyter notebook environment, run "exa" on the command line.
'''
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
    '''
    Start the exa notebook gui (a Jupyter notebook environment).
    '''
    subprocess.Popen(['jupyter notebook'], shell=True, cwd=config['paths']['notebooks'])


def workflow(wkflw):
    '''
    Args:
        wkflw: Path to workflow script or instance of workflow class.
    '''
    raise NotImplementedError('Workflows are currently unsupported.')


def main():
    '''
    Main entry point for the application.
    '''
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        '-u',
        '--update',
        action='store_true',
        help='Update static data and extensions (updates will occur on next import).'
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
        set_update()
        exatomic_up()
    elif args.workflow is None:
        notebook()
    else:
        workflow(args.workflow)


if __name__ == '__main__':
    main()
