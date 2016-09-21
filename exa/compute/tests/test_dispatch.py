# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.dispatch`
##########################################
"""
import numpy as np
from exa.compute.dispatch import dispatch
from exa.tester import UnitTester


class TestDispatcher(UnitTester):
    """
    """
    def setUp(self):
        """
        """
        # Create dispatched functions...
        try:
            @dispatch(str)
            def fn(arg):
                return arg + "!"

            @dispatch(bool)
            def fn(arg):
                return str(arg) + "!"

            @dispatch(int)
            def fn(arg):
                return str(arg) + "!"

            @dispatch((int, np.int64))
            def fn(arg):
                return str(arg) + "!"

            @dispatch(str, bool)
            def fn(arg0, arg1):
                return arg0 + str(arg1) + "!"

            @dispatch((str, int), (bool, int))
            def fn(arg0, arg1):
                return str(arg0) + str(arg1) + "!"
        except Exception as e:
            self.fail(str(e))
        self.fn = fn

    def test_single_dispatch(self):
        """
        """
        self.assertTrue(self.fn("Foo").endswith("!"))
        self.assertTrue(self.fn(True).endswith("!"))
        self.assertTrue(self.fn(42).endswith("!"))
        self.assertTrue(self.fn(np.int64(42)).endswith("!"))
        with self.assertRaises(TypeError):
            self.fn(np.int32(42))

    def test_multiple_dispatch(self):
        """Test multiply dispatched arguments."""
        self.assertTrue(self.fn("Bar", True).endswith("!"))
        self.assertTrue(self.fn(42, 42).endswith("!"))
        self.assertTrue(self.fn("42", True).endswith("!"))

    def test_nb_compiler(self):
        """
        """
        pass
