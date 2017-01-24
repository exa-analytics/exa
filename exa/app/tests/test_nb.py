# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.app.nb`
##################################
"""
from notebook.notebookapp import NotebookApp
from exa.tester import UnitTester
from exa.app.nb import Notebook


class TestNotebook(UnitTester):
    """Check the :class:`~exa.app.nb.Notebook` object."""
    def test_instance(self):
        """Type check."""
        self.assertIsInstance(Notebook, NotebookApp)
