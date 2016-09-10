# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Test for :mod:`~exa._config`
##################################
"""
import os
import sys
import shutil
import pandas as pd
if sys.version[0] == 2:
    from io import BytesIO as StringIO
else:
    from io import StringIO
from sqlalchemy.exc import OperationalError
from exa import _config
from exa.tester import UnitTester


class TestConfig(UnitTester):
    """
    This test works by temporarily reconfiguring the config object to be located
    in the "~/.exa_test" directory. When :func:`~exa._config.reconfigure` is
    called with the non-default argument (the default is ".exa") it should force
    a call to :func:`~exa._config.initialize`. Upon completion, this test reverts
    to the default configuration.
    """
    def setUp(self):
        """
        Generate the temporary test configuration.
        """
        try:
            shutil.rmtree(os.path.join(_config.config['dynamic']['home'], ".exa_test"))
        except OSError:
            pass
        _config.reconfigure(".exa_test")

    def tearDown(self):
        """
        Reset to the default configuration.
        """
        to_be_deleted = _config.config['dynamic']['root']
        _config.reconfigure()
        try:
            shutil.rmtree(to_be_deleted)
        except OSError:
            pass

    def test_mkdir(self):
        """
        Test that config created the new configuration directory.
        """
        self.assertTrue(os.path.exists(_config.config['dynamic']['root']))

    def test_db(self):
        """
        By default, the configuration creates a sqlite database in the config
        directory which stores content management and static data.
        """
        dbfile = _config.config['db']['uri'].replace("sqlite:///", "")
        self.assertTrue(os.path.isfile(dbfile))
        try:
            df = pd.read_sql("select * from isotope", con=_config.engine)
        except OperationalError:
            self.fail("Failed to select isotope data at {}.".format(_config.engine))
        self.assertTrue(len(df) > 3000)
        try:
            df = pd.read_sql("select * from time", con=_config.engine)
        except OperationalError:
            self.fail("Failed to select time data at {}.".format(_config.engine))
        self.assertTrue(len(df) > 200)
        try:
            df = pd.read_sql("select * from constant", con=_config.engine)
        except OperationalError:
            self.fail("Failed to select constant data at {}.".format(_config.engine))
        self.assertTrue(len(df) > 29)

    def test_print(self):
        """
        Test :func:`~exa._config.print_config`.
        """
        out = StringIO()
        _config.print_config(out=out)
        out = out.getvalue()
        self.assertIn("[DEFAULT]", out)

    def test_logger_head_tail(self):
        """
        Tests for custom `head` and `tail` methods on the loggers attribute of
        :mod:`~exa._config`.
        """
        _config.loggers['sys'].warning("test warning")
        out = StringIO()
        _config.loggers['sys'].tail(out=out)
        self.assertIn("test warning", out.getvalue().strip())
