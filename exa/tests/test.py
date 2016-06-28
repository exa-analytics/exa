# -*- coding: utf-8 -*-
'''
Comprehensive Test
##################################
This multifaceted test checks the ability of the base package to edit data
and create a meaningful container object using the generic functionality
provided by exa.
'''
from io import StringIO
from urllib.error import HTTPError
from urllib.request import urlopen
from exa.test import UnitTester
from exa.editor import Editor


monthly_data = 'http://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv'
zonal_data = 'http://data.giss.nasa.gov/gistemp/tabledata_v3/ZonAnn.Ts+dSST.csv'


class ComprehensiveTest(UnitTester):
    '''
    This test represents a basic example of data analysis, within the exa
    framework, with steps common to all fields of data science:

    1. Obtain data (from internet or file)
    2. Preprocess data (format, strip, trim, etc.)
    3. Create container
    4. Check data relationships and save container
    5. Plot interesting features
    6. Generate report for publication

    Data is publically available from `NASA`_.

    .. _NASA: http://data.giss.nasa.gov/gistemp/
    '''
    def setUp(self):
        '''
        Test step 1.

        This method is called first and prepares the test's data. This method
        tests the ability of the :class:`~exa.editor.Editor` to detect and load
        data from a string. For further reference on the use of this method,
        see `Python docs`_.

        .. _Python docs: https://docs.python.org/3.5/library/unittest.html
        '''
        try:
            string = urlopen(monthly_data).read().decode('utf-8')
        except HTTPError:
            with open('../_static/sample/gistemp/GLB.Ts+dSST.csv') as f:
                string = f.read()
        self.monthly_editor = Editor(string)
        try:
            string = urlopen(zonal_data).read().decode('utf-8')
        except HTTPError:
            with open('../_static/sample/gistemp/ZonAnn.Ts+dSST.csv') as f:
                string = f.read()
        self.zonal_editor = Editor(string)

    def test_step2(self):
        '''
        Test step 2.
        '''
