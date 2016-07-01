# -*- coding: utf-8 -*-
'''
Tests for :mod:`~exa.relational.container`
============================================
Because :class:`~exa.relational.container.Container` inherits
:class:`~exa.container.BaseContainer`, the functionality here may inadvertently
test the inherited class. Every effort is made to separate the tests logically.


* :class:`~exa.tests.test_container.TestBaseContainer` contains tests that
  check the methods of :class:`~exa.container.BaseContainer`
* :class:`~exa.tests.test_widget.TestWidget` contains tests that check
  the methods of :class:`~exa.widget.Widget`
* :class:`~exa.relational.tests.test_container.TestRelationalContainer` contains
  tests that check the methods of :class:`~exa.relational.container.Container`
* :class:`~exa.relational.tests.test_container.TestContainer` contains tests
  that check the functionality of :class:`~exa.relational.container.Container`
  that relies on all of the inherited classes.
'''
import os
import numpy as np
import pandas as pd
from tempfile import mkstemp
from exa.test import UnitTester
from exa.relational.container import Container


#class TestRelationalContainer(UnitTester):
#    '''
#    Test methods of :class:`~exa.relational.container.Container` that are
#    independent of functionality inherited from :class:`~exa.container.BaseContainer`.
#    '''
#    def test_table(self):
#        '''
#        Like all relational tables we should be able to call the
#        :func:`~exa.relational.base.Base.table` function.
#        '''
#        self.assertIsInstance(Container.to_frame(), pd.DataFrame)
#
#
#class TestContainer(UnitTester):
#    '''
#    Comprehensive testing of :class:`~exa.relational.container.Container`
#    including inherited functionality dependent on :class:`~exa.container.BaseContainer`.
#    '''
#    def test_save(self):
#        fd, path = mkstemp(suffix='.hdf5')
#        df = pd.DataFrame(np.random.rand(5, 5))
#        c = Container(name='test', description='created by TestContainer.test_save',
#                      df=df)
#        c.save(path)
#        self.assertTrue(c.pkid in Container.to_frame().index)
#        self.assertTrue(os.path.exists(path))
#        os.remove(path)
#
