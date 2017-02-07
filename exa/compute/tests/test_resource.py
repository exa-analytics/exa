# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.resources`
########################################################
"""
#import psutil
#import numpy as np
#from exa.tester import UnitTester
#from exa.compute.resources import (default_resources, get_ngpus, Resource,
#                                   Resources, inspect_resource, parallelize)
#
#
#class TestResource(UnitTester):
#    """Tests for :mod:`~exa.compute.resources`."""
#    def test_get_ngpus(self):
#        """Test :func:`~exa.compute.resources.get_ngpus`."""
#        self.assertIsInstance(get_ngpus(), int)
#
#    def test_inspect_resource(self):
#        """Test :func:`~exa.compute.resources.inspect_resource`."""
#        name = "name"
#        resource = inspect_resource(name)
#        self.assertIsInstance(resource, Resource)
#        self.assertEqual(resource.name, name)
#        self.assertEqual(resource.cpus, psutil.cpu_count())
#        self.assertTrue(np.isclose(resource.memory, psutil.virtual_memory().total))
#        self.assertEqual(resource.gpus, get_ngpus())
#
#    def test_default_resources(self):
#        """Test :func:`~exa.compute.resources.default_resources`."""
#        resources = default_resources()
#        self.assertIsInstance(resources, Resources)
#        self.assertEqual(len(resources), 1)
#        self.assertIsInstance(resources.resources[0], Resource)
#
#    def test_parallelize(self):
#        """Test :func:`~exa.compute.resources.parallelize`."""
#        with self.assertRaises(NotImplementedError):
#            parallelize()
