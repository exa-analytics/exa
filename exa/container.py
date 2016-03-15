# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
from traitlets import MetaHasTraits
from exa import _conf
from exa.widget import Widget
from exa.relational.base import BaseMeta
from exa.relational.container import RelationalContainer


class BaseContainer(RelationalContainer):
    '''
    The data container.
    '''
    __dfs = {}


class ContainerMeta(MetaHasTraits, BaseMeta):
    '''
    A dummy metaclass to enable inheritence from both :class:`~ipywidget.DOMWidget`
    and :class:`~exa.relational.RelationalContainer`.
    '''
    pass


class WidgetContainer(Widget, BaseContainer, metaclass=ContainerMeta):
    '''
    '''
    pass


Container = BaseContainer
if _conf['notebook']:
    Container = WidgetContainer
