# -*- coding: utf-8 -*-
'''
Dashboard
=======================
The workspace is a way to track and interact with different sets of
:class:`~exa.relational.Store` objects, which themselves that keep track of
user work. This includes :class:`~exa.relational.Program`s,
:class:`~exa.relational.Project`s, :class:`~exa.relational.Job`s,
:class:`~exa.relational.File`s, and :class:`~exa.relational.Container`s.
'''
from exa.relational import Store
from exa.relational import Container as DBContainer
from exa.container import Container
from exa.widget import Widget


class Dashboard(Widget):
    def list_stores(self):
        '''
        Listing of user's stores.
        '''
        return Store._get_all()

    def list_containers(self):
        '''
        '''
        return DBContainer._get_all()

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return 'Dashboard\n{0}'.format(self.list_stores())

Dashboard = Dashboard()
