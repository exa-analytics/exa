# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.mgmt`
#############################################
"""
import pandas as pd
from sqlalchemy.exc import IntegrityError
from exa.tester import UnitTester
from exa.cms.mgmt import init_db, init_tutorial


class TestMgmt(UnitTester):
    """Tests for :mod:`~exa.cms.mgmt`."""
    def test_init_db(self):
        """Test :func:`~exa.cms.mgmt.init_db`."""
        init_db()

    def test_init_tutorial(self):
        """Test :func:`~exa.cms.mgmt.init_tutorial`."""
        with self.assertRaises(IntegrityError):
            init_tutorial()    # UID unique constraint should fail, since tutorial exists

