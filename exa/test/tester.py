# -*- coding: utf-8 -*-
'''
Tester
#########################
Custom tester class for running interactive (i.e. within the Jupyter notebook
environment) tests.
'''
import os
import sys
from doctest import DocTestFinder, DocTestRunner
from unittest import TestCase, TestLoader, TextTestRunner
from exa.log import loggers
from exa._setup import config
from exa.utility import datetime_header


logger = loggers['syslog']    # Tests are written to the system log
verbosity = int(config['log']['level'])
verbose = True if verbosity > 0 else False


class UnitTester(TestCase):
    '''
    The custom tester class which provides an alternative test runner.
    '''
    @classmethod
    def run_interactively(cls, log=False):
        '''
        Run a test suite in a Jupyter notebook environment or shell.

        Args:
            log (bool): Write output to a log file instead of to stdout
        '''
        suite = TestLoader().loadTestsFromTestCase(cls)
        if log:
            result = TextTestRunner(logger.handlers[0].stream,
                                    verbosity=verbosity).run(suite)
        else:
            result = TextTestRunner(verbosity=verbosity).run(suite)
        return result


def run_doctests(log=False):
    '''
    Run all docstring tests.

    Args:
        log (bool): Write test results to system log (default false)
    '''
    def tester(modules, runner, f=None):
        '''Runs tests for each module.'''
        for module in modules:
            tests = DocTestFinder().find(module)
            tests.sort(key=lambda test: test.name)
            for test in tests:
                if test.examples == []:    # Skip empty tests
                    pass
                else:
                    if f:
                        f.write('\n'.join(('-' * 80, test.name, '-' * 80, '\n')))
                        runner.run(test, out=f.write)
                    else:
                        print('\n'.join(('-' * 80, test.name, '-' * 80)))
                        runner.run(test)

    runner = DocTestRunner(verbose=verbose)
    modules = [v for k, v in sys.modules.items() if k.startswith('exa')]
    modules.sort(key=lambda module: module.__file__)
    if log:
        logger.debug('LOGGING DOCTEST')
        tester(modules, runner, f=logger.handlers[0].stream)
    else:
        tester(modules, runner)


def run_unittests(log=False, verbosity=0):
    '''
    Perform (interactive) unit testing logging the results.

    Args:
        log (bool): Send results to system log (default False)
        verbosity (int): Level of verbosity for unit tests (0-2)
    '''
    tests = UnitTester.__subclasses__()
    if log:
        logger.debug('LOGGING UNITTEST')
    for test in tests:
        test.run_interactively(log=log, verbosity=verbosity)
