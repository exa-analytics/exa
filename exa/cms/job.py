# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Job Table
#############
A job is a single experiment, typically resulting in a number of "raw" data
files (inputs and outputs). A job can often be organized in a single container
object.
"""
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import relationship
from exa.cms.base import Name, Time, Size, Base, Sha256UID


job_file = Table(    # Many to many relationship; Job - File
    'job_file',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE',
                                           ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE',
                                            ondelete='CASCADE'))
)


class Job(Name, Time, Size, Sha256UID, Base):
    """
    A single computational experiment that generates one or more output files.
    """
    files = relationship('File', secondary=job_file, backref='jobs',
                         cascade='all, delete')