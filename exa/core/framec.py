# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Frame Container
######################################
TODO
"""
from exa.core.container import ABCContainer


class FrameContainer(ABCContainer):
    """
    TODO
    """
    def concat(self):
        return True

    def describe(self):
        return True

    def _html_repr_(self):
        return True
