# -*- coding: utf-8 -*-
'''
Comprehensive Test
##################################
This multifaceted test checks the ability of the base package to edit data
and create a meaningful container object using the generic functionality
provided by exa.
'''
#from io import StringIO
#from urllib.error import HTTPError
#from urllib.request import urlopen
#from exa import Editor, Series, DataFrame
#from exa.test import UnitTester

#import numpy as np
#import pandas as pd
##from sqlalchemy import Column, Integer,
#from exa import Container
#from exa.container import TypedMeta
#from exa.relational.base import BaseMeta
#from exa.widget import ContainerWidget
#from exa.numerical import Series, DataFrame, SparseSeries, SparseDataFrame, Field3D
#from exa.test import UnitTester
#
#
#class TestSeries0(Series):
#    '''
#    Series object where the index name is always "idx".
#    '''
#    _precision = 2
#    _sname = 's0'
#
#
#class TestSeries1(Series):
#    '''
#    Series object where the index name is always "idx".
#    '''
#    _precision = 2
#    _sname = 's1'
#    _iname = 's1idx'
#    _index_trait = True
#    _stype = str
#    _itype = np.int64
#
#
#class TestDataFrame(DataFrame):
#    '''
#    Test dataframe object tracks 3D objects of a given shape at
#    a given origin.
#    '''
#    _groupbys = ['group']
#    _indices = ['obj']
#    _columns = ['x', 'y', 'z', 'typ']
#    _traits = ['x', 'y', 'z']
#    _categories = {'group': np.int64, 'typ': str}
#    _precision = {'x': 2, 'y': 2, 'z': 2}
#
#
#class TestField(Field3D):
#    _vprecision = 6
#
#
#class TestContainerTypes(TypedMeta):
#    '''Statically typed attributes'''
#    s0 = TestSeries0
#    s1 = TestSeries1
#    df = TestDataFrame
#
#
#class TestMeta(TestContainerTypes, BaseMeta):
#    pass
#
#
#class TestContainer(Container, metaclass=TestContainerTypes):
#    '''
#    The test container has
#    '''
##    tcid = Column(Integer, ForeignKey('container.pkid'), primary_key=True)
##    __mapper_args__ = {'polymorphic_identity': 'testcontainer'}
#    _widget_class = ContainerWidget
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        x = [0, 1, 2, 3, 4]
#        y = [0, 0, 0, 0, 0]
#        z = [0.5, 1.5, 2.5, 3.5, 4.5]
#        typ = ['cube', 'sphere', 'cube', 'sphere', 'cube']
#        group = [0, 0, 1, 1, 1]
#        self.s1 = TestSeries1(typ, dtype='category')
#        self.s0 = TestSeries0([1.1, 2.2, 3.3, 4.4, 5.5])
#        self.df = TestDataFrame.from_dict({'x': x, 'y': y, 'z': z, 'typ': typ, 'group': group})
#        self._test = False
#
#
#class TestRandom(UnitTester):
#    def setUp(self):
#        self.c = TestContainer()
#
#    def test_series_names(self):
#        '''
#        Test auto/default naming of :class:`~exa.numerical.Series` objects.
#        '''
#        self.assertEqual(self.c.s0.name, 's0')
#        self.assertIsNone(self.c.s0.index.name)
#        self.assertEqual(self.c.s1.name, 's1')
#        self.assertEqual(self.c.s1.index.name, 's1idx')
#
#    def test_trait_creation(self):
#        '''
#        Ensure that traits are being created for the container.
#        '''
#        self.c._update_traits()
#
#
#monthly_data = 'http://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv'
#zonal_data = 'http://data.giss.nasa.gov/gistemp/tabledata_v3/ZonAnn.Ts+dSST.csv'
#
#
##class TestRealData(UnitTester):
##    '''
##    This test represents a basic example of data analysis, within the exa
##    framework, with steps common to all fields of data science:
##
##    1. Obtain data (from internet or file)
##    2. Preprocess data (format, strip, trim, etc.)
##    3. Create container
##    4. Check data relationships and save container
##    5. Plot interesting features
##    6. Generate report for publication
##
##    Data is publically available from `NASA`_.
##
##    .. _NASA: http://data.giss.nasa.gov/gistemp/
##    '''
##    def setUp(self):
##        '''
##        Test step 1.
##
##        This method is called first and prepares the test's data. This method
##        tests the ability of the :class:`~exa.editor.Editor` to detect and load
##        data from a string. For further reference on the use of this method,
##        see `Python docs`_.
##
##        .. _Python docs: https://docs.python.org/3.5/library/unittest.html
##        '''
##        try:
##            string = urlopen(monthly_data).read().decode('utf-8')
##        except HTTPError:
##            with open('../_static/sample/gistemp/GLB.Ts+dSST.csv') as f:
##                string = f.read()
##        self.monthly_editor = Editor(string)
##        try:
##            string = urlopen(zonal_data).read().decode('utf-8')
##        except HTTPError:
##            with open('../_static/sample/gistemp/ZonAnn.Ts+dSST.csv') as f:
##                string = f.read()
##        self.zonal_editor = Editor(string)
##
##    def test_step2(self):
##        '''
##        Test step 2.
##        '''
##        pass
##
#
