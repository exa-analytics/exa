# -*- coding: utf-8 -*-
'''
Physical Constants
===============================================
'''
from exa.relational import Base, Column, String, Float


class Constant(Base):
    '''
    Physical constants.
    '''
    symbol = Column(String, nullable=False)
    value = Column(Float, nullable=False)
