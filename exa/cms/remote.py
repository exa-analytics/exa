# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Remote Resources
##################
Remote resources, such as a super computer, accessible over SSH.
"""
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from exa.cms.base import Base


class RemoteResource(Base):
    """
    A remote (super) computer accessible over SSH.

    Attributes:
        username (str): Username
        headnode (str): Machine address used for executing commands (192.168.1.1:22)
        transfer (str): Address of machine used for data transfer (if different. 192.168.1.2:22)
        scratch (str): User's global scratch space (or environment variable)
        project (str): User's group's persistent project space
        user (str): User's space
    """
    username = Column(String)
    headnode = Column(String)
    transfer = Column(String)
    scratch = Column(String)
    project = Column(String)
    user = Column(String)

    def connect(self):
        """Establish an SSH connection."""
        raise NotImplementedError()
