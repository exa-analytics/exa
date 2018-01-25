# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
#import numpy as np
#import matplotlib as mpl
#from unittest import TestCase
#from exa.util.mpl import _gen_figure
#
#
#class TestGenFigure(TestCase):
#    """Test matplotlib wrapper function. Needs work."""
#    def setUp(self):
#        """Make some figures."""
#        self.fig1 = _gen_figure(nxplot=1, nyplot=2, x=np.array([0, 1, 2]),
#                                nxlabel=5, nxdecimal=3, sharex=True, sharey=True)
#        self.fig2 = _gen_figure(nxplot=2, nyplot=1, projection='3d')
#        self.fig3 = _gen_figure(nxplot=1, nyplot=1, projection='polar')
#
#    def test_2d_plot(self):
#        """Test shared axes."""
#        ax = self.fig1.get_axes()[0]
#        self.assertTrue('_sharex' in ax.__dict__)
#        self.assertTrue('_sharey' in ax.__dict__)
#
#    def test_3d_plot(self):
#        """Test 3D axes."""
#        self.assertTrue(self.fig2.get_axes()[0].__dict__['_axis3don'])
#
#    def test_polar_plot(self):
#        """Test polar axes."""
#        self.assertTrue('_theta_offset' in self.fig3.get_axes()[0].__dict__)
