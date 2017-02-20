# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.dispatcher`
##########################################
"""
import numpy as np
from exa.compute.dispatcher import dispatch, Dispatcher, arg_count
from exa.tester import UnitTester


class TestDispatcher(UnitTester):
    """Tests for multiple dispatching."""
    pass
#    def test_arg_count(self):
#        """Test :func:`~exa.compute.dispatcher.arg_count`."""
#        def f(a):
#            pass
#        self.assertEqual(arg_count(f), 1)
#        def f(a, b):
#            pass
#        self.assertEqual(arg_count(f), 2)
#        def f(a, b=None):
#            pass
#        self.assertEqual(arg_count(f), 2)
#
#
#    def test_manual(self):
#        """Test 'by hand' dispatcher creation."""
#        f = Dispatcher("f")
#        #f.register(lambda x: x.zfill(2), str)  # Same as @dispatch(str)...
#        #print(f("1"))
#        #self.assertEqual(f("1"), "01")
