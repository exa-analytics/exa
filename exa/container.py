# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
from sqlalchemy import Column, Integer, ForeignKey
from exa import _conf
from exa.widget import Widget, _Meta
from exa.relational import _create_all
from exa.relational.container import Container as _Container


class BasicContainer(_Container):
    '''
    The data container.

    This container is one part object based storage device, one part relational
    storage, and one part data analysis.

    See Also:
        :class:`~exa.relational.container.Container`
    '''
    cid = Column(Integer, ForeignKey('container.pkid'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'basic_container'}
    __dfs = {}


class WidgetContainer(Widget, BasicContainer, metaclass=_Meta):
    '''
    See Also:
        :class:`~exa.widget.Widget`
    '''
    cid = Column(Integer, ForeignKey('container.pkid'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'widget_container'}



# Here we alias the working container based on the current environment
Container = WidgetContainer if _conf['notebook'] else BasicContainer
