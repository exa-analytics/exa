# -*- coding: utf-8 -*-
'''
Doc and Unit Testing
#########################
Extends the functionality of standard documentation and unit testing for use
inside the Jupyter notebook (interactive testing) and automatic logging.
'''
import os
import sys
sys.path.insert(0, os.path.abspath('.'))    # Allows code to run from repository
from doctest import DocTestFinder, DocTestRunner
from unittest import TestCase, TestLoader, TextTestRunner
from exa._config import config
from exa.log import get_logger
from exa.utility import datetime_header


logger = get_logger('sys')


class UnitTester(TestCase):
    '''
    Adds interactive testing to unittest. This class should be inherited by all
    TestCase-like classes that are part of exa's internal test suite.
    '''
    @classmethod
    def run_interactively(cls, log=False, verbosity=0):
        '''
        Run a test suite interactively (e.g. in an IPython notebook) as well as
        from command line.

        Args:
            log (bool): Write output to a log file instead of to stdout

        Returns:
            result (:class:`~unittest.TestResult`): Test result
        '''
        suite = TestLoader().loadTestsFromTestCase(cls)
        result = None
        if log:
            result = TextTestRunner(logger.handlers[0].stream,
                                    verbosity=verbosity).run(suite)
        else:
            result = TextTestRunner(verbosity=verbosity).run(suite)
        return result


class TestTester(UnitTester):
    '''
    Functions that test the :class:`~exa.test.UnitTester` itself as well as
    foundational modules, :mod:`~exa._config`, :mod:`~exa.log`,
    and :mod:`~exa.utility`.
    '''
    def test_config(self):
        '''
        Check that access to the configuration object is possible and that
        the root exa directory and relational database exist.
        '''
        self.assertIsInstance(config, dict)
        self.assertIn('exa_root', config)
        self.assertTrue(os.path.exists(config['exa_root']))

    def test_log(self):
        '''
        Check that log file paths are accessible.
        '''
        path = config['log_sys']
        self.assertTrue(os.path.exists(path))

    def test_utility(self):
        '''
        Check that the datetime_header imported correctly.
        '''
        self.assertTrue(hasattr(datetime_header, '__call__'))


def run_doctests(verbose=False, log=False):
    '''
    Perform (interactive) doc(string) testing logging the results.

    Args:
        verbose (bool): Verbose output (default false)
        log (bool): If True, write output to log file rather than screen.
    '''
    def tester(modules, runner, f=None):
        '''
        Helper function that iterates over all modules and runs
        all available tests.
        '''
        for module in modules:
            tests = DocTestFinder().find(module)
            tests.sort(key=lambda test: test.name)
            for test in tests:
                if test.examples == []:    # Skip empty tests
                    pass
                else:
                    if f:
                        #f.write('\n'.join(('-' * 80, test.name, '-' * 80, '\n')))
                        runner.run(test, out=f.write)
                    else:
                        #print('\n'.join(('-' * 80, test.name, '-' * 80)))
                        runner.run(test)

    runner = DocTestRunner(verbose=verbose)
    modules = [v for k, v in sys.modules.items() if k.startswith('exa')]
    modules.sort(key=lambda module: module.__file__)
    if log:
        logger.info('LOGGING DOCTTEST')
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
        logger.info('LOGGING UNITTEST')
    for test in tests:
        test.run_interactively(log=log, verbosity=verbosity)
