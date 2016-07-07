#! /usr/bin/env python
'''
Application Launchers
########################
'''
import subprocess
import unittest
import doctest
from exa._setup import config


def notebook():
    '''
    Start the exa notebook gui (a Jupyter notebook environment).
    '''
    subprocess.Popen(['jupyter notebook'], shell=True, cwd=config['paths']['notebooks'])


def workflow():
    raise NotImplementedError('Workflows are currently unsupported.')


if __name__ == '__main__':
    notebook()
