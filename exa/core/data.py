# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data
########
"""
from traitlets import Unicode, Integer, Float
from traitlets.config import Configurable

from exa import Base


class Data(Base, Configurable):
    myvar = Integer(5).tag(config=True)
