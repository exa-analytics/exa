# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
File Table
###################
The file table keeps a record of all files (on disk) managed by the exa framework.
"""
from sqlalchemy import String, Column, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from exa._config import config
from exa.cms.base import Base, Name, HexUID, Time


class File(Name, HexUID, Time, Base):
    """
    Representation of a non exa container file on disk. Provides content
    management for "raw" data files.
    """
    extension = Column(String, nullable=False)    # File extension
    size = Column(Integer)
    container = Column(String)    # container type (i.e. class name)

    def get_size(self):
        pass


if '_tut_file' in config['dynamic']:
    tutorial = File(name="tutorial.ipynb")
