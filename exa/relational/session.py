# -*- coding: utf-8 -*-
'''
Session
===============================================
'''
from sqlalchemy import ForeignKey, Table, Column, Integer
from sqlalchemy.orm import relationship
from exa import Config
from exa.relational.base import db_sess, Base, Name, HexUID, Time, Disk
from exa.utils import gen_uid


#SessionProgram = Table(
#    'sessionprogram',
#    Base.metadata,
#    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
#    Column('program_pkid', Integer, ForeignKey('program.pkid', onupdate='CASCADE', ondelete='CASCADE'))
#)
#
#
#SessionProject = Table(
#    'sessionproject',
#    Base.metadata,
#    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
#    Column('project_pkid', Integer, ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE'))
#)
#
#
#SessionJob = Table(
#    'sessionjob',
#    Base.metadata,
#    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
#    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE'))
#)


SessionContainer = Table(
    'sessioncontainer',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


SessionFile = Table(
    'sessionfile',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Session(Name, HexUID, Time, Disk, Base):
    '''
    A :class:`~exa.relational.session.Session` keeps track of the user's active
    program, project, job, and container (active objects are not required to
    be present).
    '''
    #programs = relationship('Program', secondary=SessionProgram, backref='sessions', cascade='all, delete')
    #projects = relationship('Project', secondary=SessionProject, backref='sessions', cascade='all, delete')
    #jobs = relationship('Job', secondary=SessionJob, backref='sessions', cascade='all, delete')
    containers = relationship('Container', secondary=SessionContainer, backref='sessions', cascade='all, delete')
    files = relationship('File', secondary=SessionFile, backref='sessions', cascade='all, delete')

    def __repr__(self):
        if self.name == 'anonymous':
            return 'Session({0}: anonymous[{1}])'.format(self.pkid, str(self.accessed).split('.')[0])
        elif self.name is None:
            return 'Session({0}: {1})'.format(self.pkid, self.uid)
        else:
            return 'Session({0}: {1})'.format(self.pkid, self.name)


def cleanup_sessions():
    '''
    Only the N (default: 5) most recent (anonymous) exa sessions are stored
    in the database. On exit, the oldest anonymous sessions (and their data
    on disk) are permanently deleted.

    Note:
        The value of N is defined by exa's configuration (:class:`~exa.config.Config`).
    '''
    anons = db_sess.query(Session).filter(
        Session.name == 'anonymous'
    ).order_by(Session.accessed).all()[:-Config.max_anon_sessions]
    for anon in anons:
        db_sess.delete(anon)
