# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
File Table
###################
The file table keeps a record of all files (on disk) managed by the exa framework.
"""
import os
import shutil
from datetime import datetime
from sqlalchemy import String, Column, Integer, Table, ForeignKey
from exa.cms.base import Base, Name, Sha256UID, Time
from exa.cms.errors import FileCreationError
from exa._config import config, mkdir


class File(Name, Time, Sha256UID, Base):
    """
    Representation of a non exa container file on disk. Provides content
    management for "raw" data files.
    """
    ext = Column(String, nullable=False)    # File extension (no ".")
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
            raise OSError("File not found: {}".format(path))
        prefix, ext = os.path.splitext(path)
        ext = ext[1:]    # Remove the leading "."
        name = os.path.basename(prefix)
        size = os.path.getsize(path)
        uid = cls.sha256_from_file(path)
        modified = datetime.fromtimestamp(os.path.getmtime(path))
        obj = cls(name=name, size=size, ext=ext, uid=uid, modified=modified,
                  **kwargs)
        mkdir(os.path.dirname(obj.path))
        shutil.copyfile(path, obj.path)
        return obj

    @property
    def path(self):
        """Get the file path of the current file."""
        return os.path.join(data_dir, self.ext, self.uid)

    @property
    def all_projects(self):
        """Check if this file has a second relation to a project."""
        projects = []
        for job in self.jobs:
            projects += job.projects
        return projects


data_dir = config['paths']['data']
del config
