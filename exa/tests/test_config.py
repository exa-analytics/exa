# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa._config`
##################################
Test config, logging, and database engine manipulation.
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
from exa import _config, _jupyter_nbextension_paths
from exa._config import _j
from exa.tester import UnitTester


class TestConfig(UnitTester):
    """
    All tests are performed in a temporary configuration space '.exa_test' so
    as not to affect working configuration.
    """
    def setUp(self):
        """Generate the temporary test configuration."""
        try:
            shutil.rmtree(_j(_config.config['dynamic']['home'], ".exa_test"))
        except OSError:
            pass

    def tearDown(self):
        """Delete test configurations."""
        path = _j(_config.config['dynamic']['home'], ".exa_test")
        _config.engine.dispose()
        _config.reconfigure()
        try:
            shutil.rmtree(path)
        except OSError:
            raise
            pass

    def test_reconfigure(self):
        """Test generation of config.ini."""
        _config.reconfigure(".exa_test")
        _config.config['logging']['level'] = "1"
        self.assertEqual(_config.config['logging']['level'], "1")
        _config.reconfigure(".exa_test")
        _config.config['logging']['level'] = "2"
        self.assertEqual(_config.config['logging']['level'], "2")
        _config.save(del_dynamic=False)
        config_file = _j(config['dynamic']['home'], ".exa_test", "config.ini")
        dynamic = False
        with open(config_file) as f:
            for line in f:
                if "[dynamic]" in line:
                    dynamic = True
                    break
        self.assertTrue(dynamic)
        _config.reconfigure(".exa_test")
        self.assertEqual(_config.config['logging']['level'], "0")

    def test_mkdir(self):
        """Test that config created the new configuration directory."""
        self.assertTrue(os.path.exists(_config.config['dynamic']['root']))

    def test_db(self):
        """
        By default, the configuration creates a sqlite database in the config
        directory which stores content management and static data.
        """
        df = pd.read_sql("select * from isotope", con=_config.engine)
        self.assertIsInstance(df, pd.DataFrame)
        df = pd.read_sql("select * from constant", con=_config.engine)
        self.assertIsInstance(df, pd.DataFrame)

    def test_print(self):
        """Test :func:`~exa._config.print_config`."""
        out = StringIO()
        _config.print_config(out=out)
        out = out.getvalue()
        self.assertIn("[DEFAULT]", out)

    def test_logger_head_tail(self):
        """
        Tests for custom `head` and `tail` methods on the loggers attribute of
        :mod:`~exa._config`.
        """
        _config.loggers['sys'].warning("THIS IS A TEST")
        out = StringIO()
        _config.loggers['sys'].head(out=out)
        _config.loggers['sys'].tail(out=out)
        self.assertIn("THIS IS A TEST", out.getvalue().strip())

    def test_save(self):
        """Test :func:`~exa._config.save`."""
        _config.save(True)

    def test_init_function(self):
        """Test build related function."""
        obj = _jupyter_nbextension_paths()
        self.assertIsInstance(obj, list)

