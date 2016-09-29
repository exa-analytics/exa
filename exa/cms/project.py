# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Project Table
#################
A project represents a continuous or finite study of a subject matter. It is
the highest level of categorical organization for the content management
system.

See Also:
    :mod:`~exa.relational.job` and :mod:`~exa.relational.file`
"""
from sqlalchemy import Integer, Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from exa.cms.base import Base, Name, Time, Size


projectjob = Table(   # Many to many relationship; Project - Job
    'projectjob',
    Base.metadata,
    Column(
        'project_pkid',
        Integer,
        ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE')
    ),
    Column(
        'job_pkid',
        Integer,
        ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE')
    )
)


projectdatafile = Table(    # Many to many relationship; Project - DataFile
    'projectdatafile',
    Base.metadata,
    Column(
        'project_pkid',
        Integer,
        ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE')
    ),
    Column(
        'datafile_pkid',
        Integer,
        ForeignKey('datafile.pkid', onupdate='CASCADE', ondelete='CASCADE')
    )
)


projectcontainerfile = Table(    # Many to many relationship; Project - ContainerFile
    'projectcontainerfile',
    Base.metadata,
    Column(
        'project_pkid',
        Integer,
        ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE')
    ),
    Column(
        'containerfile_pkid',
        Integer,
        ForeignKey('containerfile.pkid', onupdate='CASCADE', ondelete='CASCADE')
    )
)


class Project(Name, Time, Size, Base):
    """Continuous or finite study of a certain subject with a specific goal."""
    jobs = relationship('Job', secondary=projectjob, backref='projects',
                        cascade='all, delete')
    containerfiles = relationship('ContainerFile', secondary=projectcontainerfile,
                                  backref='projects', cascade='all, delete')
    datafiles = relationship('DataFile', secondary=projectdatafile,
                             backref='projects', cascade='all, delete')
