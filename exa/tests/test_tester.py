# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Test for :mod:`~exa.tester`
##################################
Tests for Exa's custom test runners.
"""
from unittest.result import TestResult
from exa.tester import UnitTester, datetime_header, get_internal_modules
from exa.tester import run_doctests, run_unittests, run_all_tests
from exa.tests.test_errors import TestExceptions


class TestTester(UnitTester):
    """
    Tests for :mod:`~exa.tester`.
    """
    def test_datetime_header(self):
        """
        Test for :func:`~exa.tester.datetime_header`.
        """
        results = datetime_header("test")
        self.assertIn("test", results)

    def test_get_internal_modules(self):
        """
        Test for :func:`~exa.tester.get_internal_modules`.
        """
        results = get_internal_modules()
        self.assertIsInstance(results, list)

    def test_runners(self):
        """
        Test for :func:`~exa.tester.run_unittests` and
        :func:`~exa.tester.run_doctests`.
        """
        results = run_unittests(mock=True)
        self.assertIsInstance(results, list)
        results = run_doctests(mock=True)
        self.assertIsInstance(results, list)

    def test_run_all(self):
        """Also tests mocking functionality."""
        tup = run_all_tests(mock=True)
        self.assertIsInstance(tup, tuple)

    def test_doc_test_logging(self):
        """Doc tests are quick so run them with logging."""
        results = run_doctests(log=True)
        self.assertIsInstance(results, list)
        result = TestExceptions.run_interactively(log=True)
        self.assertIsInstance(result, TestResult)
