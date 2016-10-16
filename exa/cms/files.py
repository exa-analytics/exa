# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
File Table
###################
The file table keeps a record of all files (on disk) managed by the exa framework.
"""
import os
from sqlalchemy import String, Column, Integer, Table, ForeignKey
from exa.cms.base import Base, Name, Sha256UID, Time


class File(Name, Time, Sha256UID, Base):
    """
    Representation of a non exa container file on disk. Provides content
    management for "raw" data files.
    """
    ext = Column(String, nullable=False)    # File extension
    size = Column(Integer)
    container = Column(String)    # container type (i.e. class name)

    @classmethod
    def from_path(cls, path, **kwargs):
        """
        Create a file entry using a file path on disk.

        Args:
            path (str): Full file path
        """
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        prefix, ext = os.path.splitext(path)
        name = os.path.basename(path)
        size = os.path.getsize(path)
        uid = cls.sha256_from_file(path)
        return cls(name=name, size=size, ext=ext, uid=uid, **kwargs)
