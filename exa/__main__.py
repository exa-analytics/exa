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
import subprocess
import unittest
import doctest
from exa._config import config


def notebook():
    '''
    Start the exa notebook gui (a Jupyter notebook environment).
    '''
    subprocess.Popen(['jupyter notebook'], shell=True, cwd=config['paths']['notebooks'])


def workflow():
    raise NotImplementedError('Workflows are currently unsupported.')


if __name__ == '__main__':
    notebook()
