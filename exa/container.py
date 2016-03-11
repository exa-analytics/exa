# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
from traitlets import MetaHasTraits
from ipywidgets import DOMWidget
from exa import _conf
from exa.relational.base import Meta
from exa.relational.container import RelationalContainer


class BaseContainer(RelationalContainer):
    '''
    '''
    __tablename__ = 'container'


class ContainerMeta(traitlets.MetaHasTraits, Meta):
    '''
    '''
    pass


class WidgetContainer(_Container, DOMWidget, metaclass=ContainerMeta):
    '''
    '''
    __tablename__ = 'container'


Container = BaseContainer
if _conf['notebook]:
    Container = WidgetContainer
