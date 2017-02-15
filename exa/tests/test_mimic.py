# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.mimic`
##################################
Tests for mimicked classes
"""
from exa.tester import UnitTester
from exa.mimic import Mimic


class TestMimic(UnitTester):
    """
    Tests that we can mimic a range of objects as well as mimic mimicked objects.
    """
    def setUp(self):
        self.non = None
        self.sca = 1
        self.lst = ['a', 'b', 3]
        self.tup = ('a', 'b', 3)
        self.dct = {'a': 0, 'b': 1, 3: 2}
        self.mmc = Mimic(None)
#        self.cpx =
        self.mc_non = Mimic(self.non)
        self.mc_sca = Mimic(self.sca)
        self.mc_lst = Mimic(self.lst)
        self.mc_tup = Mimic(self.tup)
        self.mc_dct = Mimic(self.dct)
#        self.
