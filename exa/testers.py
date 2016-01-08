# -*- coding: utf-8 -*-
'''
Testers
==================
Functionality for systematic unittests and doctests
'''
import unittest
import doctest
from exa import sys
from exa import datetime
from exa import get_logger


DOCTESTLOG = get_logger('doctest').handlers[0].baseFilename
UNITTESTLOG = get_logger('unittest').handlers[0].baseFilename


def header():
    return '\n'.join(('=' * 80, str(datetime.now()), '=' * 80))


class UnitTester(unittest.TestCase):
    '''
    Adds interactive testing to unittest. This class should be inherited by all
    TestCase-like classes that are part of exa's internal test suite.
    '''
    @classmethod
    def run_interactively(cls, log=False):
        '''
        Run a test suite interactively (e.g. in an IPython notebook).

        Args
            log (bool): Write output to a log file instead of to stdout

        Returns
            result (:class:`unittest.TestResult`): Test result
        '''
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        result = None
        if log:
            with open(UNITTESTLOG, 'a') as f:
                result = unittest.TextTestRunner(f, verbosity=2).run(suite)
        else:
            result = unittest.TextTestRunner(verbosity=2).run(suite)
        return result


def run_unittests(log=False):
    '''
    Execute all exa unit tests loaded in the current session.

    Args
        log (bool): If True, write output to log file rather than screen.
    '''
    tests = UnitTester.__subclasses__()
    if log:
        with open(UNITTESTLOG, 'a') as f:
            f.write(header())
    for test in tests:
        test.run_interactively(log=log)


def run_doctests(verbose=True, log=False):
    '''
    Execute all exa doc tests loaded in the current session.

    Args
        verbose (bool): Verbose output (default True)
        log (bool): If True, write output to log file rather than screen.
    '''
    def tester(modules, runner, f=None):
        '''
        Helper function that iterates over all modules and runs
        all available tests.
        '''
        for module in modules:
            tests = doctest.DocTestFinder().find(module)
            tests.sort(key=lambda test: test.name)
            for test in tests:
                if test.examples == []:    # Skip empty tests
                    pass
                else:
                    if f:
                        f.write('\n'.join(('-' * 80, test.name, '-' * 80)))
                        runner.run(test, out=f.write)
                    else:
                        print('\n'.join(('-' * 80, test.name, '-' * 80)))
                        runner.run(test)
    # Get the runner and modules to test
    runner = doctest.DocTestRunner(verbose=verbose)
    modules = [v for k, v in sys.modules.items() if k.startswith('exa')]
    modules.sort(key=lambda module: module.__file__)
    if log:
        with open(DOCTESTLOG, 'a') as f:
            f.write(header())
            tester(modules, runner, f=f)
    else:
        print(header())
        tester(modules, runner)


del get_logger
