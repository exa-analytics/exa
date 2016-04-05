# -*- coding: utf-8 -*-
'''
Unit and Doc Testing Base Classes
==================================
Extends the functionality of standard documentation and unit testing for use
inside the Jupyter notebook (interactive testing) and automatic logging.
'''
import sys
import doctest
import unittest
from exa.log import get_logfile_path
from exa.utility import datetime_header


log_sys = get_logfile_path('log_sys')


class UnitTester(unittest.TestCase):
    '''
    Adds interactive testing to unittest. This class should be inherited by all
    TestCase-like classes that are part of exa's internal test suite.
    '''
    @classmethod
    def run_interactively(cls, log=False):
        '''
        Run a test suite interactively (e.g. in an IPython notebook).

        Args:
            log (bool): Write output to a log file instead of to stdout

        Returns:
            result (:class:`unittest.TestResult`): Test result
        '''
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        result = None
        if log:
            with open(log_sys, 'a') as f:
                f.write(datetime_header())
                result = unittest.TextTestRunner(f, verbosity=2).run(suite)
        else:
            result = unittest.TextTestRunner(verbosity=2).run(suite)
        return result


class TestTester(UnitTester):
    '''
    Functions that test the :class:`~exa.test.UnitTester` itself as well as
    foundational modules, :mod:`~exa._config`, :mod:`~exa._log`,
    and :mod:`~exa.utility`.
    '''
    def test_config(self):
        '''
        Check that access to the configuration object is possible and that
        the root exa directory and relational database exist.
        '''
        import os
        from exa._config import _conf
        self.assertIsInstance(_conf, dict)
        self.assertIn('exa_root', _conf)
        self.assertTrue(os.path.exists(_conf['exa_root']))
        del os, _conf

    def test_log(self):
        '''
        Check that log file paths are accessible.
        '''
        import os
        from exa.log import get_logfile_path
        path = get_logfile_path(name='log_sys')
        self.assertTrue(os.path.exists(path))
        del os, get_logfile_path

    def test_utility(self):
        '''
        Check that the datetime_header imported correctly.
        '''
        self.assertTrue(hasattr(datetime_header, '__call__'))


def run_doctests(verbose=True, log=False):
    '''
    Perform (interactive) doc(string) testing logging the results.

    Args:
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

    runner = doctest.DocTestRunner(verbose=verbose)
    modules = [v for k, v in sys.modules.items() if k.startswith('exa')]
    modules.sort(key=lambda module: module.__file__)
    if log:
        with open(log_sys, 'a') as f:
            f.write(datetime_header())
            tester(modules, runner, f=f)
    else:
        tester(modules, runner)


def run_unittests(log=False):
    '''
    Perform (interactive) unit testing logging the results.

    Args:
        log (bool): Send results to system log (default False)
    '''
    tests = UnitTester.__subclasses__()
    if log:
        with open(testlog, 'a') as f:
            f.write(datetime_header())
    for test in tests:
        test.run_interactively(log=log)
