# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tester
#########################
Custom tester class for running interactive (i.e. within the Jupyter notebook
environment) tests.
"""
import os
import sys
from datetime import datetime
from doctest import DocTestFinder, DocTestRunner
from unittest import TestCase, TestLoader, TextTestRunner
from exa._config import config, loggers


logger = loggers['sys']
verbosity = int(config['logging']['level'])
verbose = True if verbosity > 0 else False


def datetime_header(title=''):
    """
    Creates a simple header string containing the current date/time stamp
    delimited using "=".
    """
    return '\n'.join(('=' * 80, title + ': ' + str(datetime.now()), '=' * 80))


def get_internal_modules(key='exa'):
    """
    Get a list of modules belonging to the given package.

    Args:
        key (str): Package or library name (e.g. "exa")
    """
    key += '.'
    return [v for k, v in sys.modules.items() if k.startswith(key)]


def run_doctests(log=False, mock=False):
    """
    Run all docstring tests.

    Args:
        log (bool): Write test results to system log (default false)
    """
    def tester(modules, runner):
        """Runs tests for each module."""
        results = []
        for module in modules:
            tests = DocTestFinder().find(module)
            tests.sort(key=lambda test: test.name)
            for test in tests:
                if mock:
                    results.append(None)
                elif test.examples == []:    # Skip empty tests
                    pass
                elif log != False:
                    f = log.handlers[0].stream
                    f.write('\n'.join(('-' * 80, test.name, '-' * 80, '\n')))
                    results.append(runner.run(test, out=f))
                else:
                    print('\n'.join(('-' * 80, test.name, '-' * 80)))
                    results.append(runner.run(test))
        return results
    runner = DocTestRunner(verbose=verbose)
    modules = get_internal_modules()
    return tester(modules, runner)


def run_unittests(log=False, mock=False):
    """
    Perform (interactive) unit testing logging the results.

    Args:
        log (bool): Send results to system log (default False)
    """
    tests = UnitTester.__subclasses__()
    if mock:
        return tests
    return [test.run_interactively(log=log) for test in tests]


class UnitTester(TestCase):
    """
    The custom tester class which provides an alternative test runner.
    """
    @classmethod
    def run_interactively(cls, log=False):
        """
        Run a test suite in a Jupyter notebook environment or shell.

        Args:
            log (bool): Write output to a log file instead of to stdout
        """
        suite = TestLoader().loadTestsFromTestCase(cls)
        if log:
            result = TextTestRunner(logger.handlers[0].stream,
                                    verbosity=verbosity).run(suite)
        else:
            result = TextTestRunner(verbosity=verbosity).run(suite)
        return result
