# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Job Table
#############
A job is a single experiment, typically resulting in a number of "raw" data
files (inputs and outputs) that can be represented in memory by a single
container. Since this is not always the case, jobs have a many to many
relationship with container files.
'''
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import relationship
from exa.relational.base import Name, Time, Size, Base


jobdatafile = Table(    # Many to many relationship; Job - DataFile
    'jobdatafile',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('datafile_pkid', Integer, ForeignKey('datafile.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


jobcontainerfile = Table(    # Many to many relationship; Job - ContainerFile
    'jobcontainerfile',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('containerfile_pkid', Integer, ForeignKey('containerfile.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Job(Name, Time, Size, Base):
    '''
    Specific task in a :class:`~exa.relational.Program` or
    :class:`~exa.relational.Project`.
    '''
    datafiles = relationship('DataFile', secondary=jobdatafile, backref='jobs',
                             cascade='all, delete')
    containerfiles = relationship('ContainerFile', secondary=jobcontainerfile,
                                  backref='jobs', cascade='all, delete')
