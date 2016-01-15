# -*- coding: utf-8 -*-
'''
Session
===============================================
'''
from exa import Config
from exa.relational.base import session, datetime, relationship
from exa.relational.base import Column, Integer, String, DateTime
from exa.relational.base import ForeignKey, Table, Base
from exa.utils import gen_uid


SessionProgram = Table(
    'sessionprogram',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('program_pkid', Integer, ForeignKey('program.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


SessionProject = Table(
    'sessionproject',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('project_pkid', Integer, ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


SessionJob = Table(
    'sessionjob',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


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


class Session(Base): #, metaclass=SessionMeta):
    '''
    Database representation of the 'session' concept.

    See Also:
        :class:`~exa.session.Session`
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    uid = Column(String(32), default=gen_uid)
    size = Column(Integer)
    file_count = Column(Integer)
    programs = relationship('Program', secondary=SessionProgram, backref='sessions', cascade='all, delete')
    projects = relationship('Project', secondary=SessionProject, backref='sessions', cascade='all, delete')
    jobs = relationship('Job', secondary=SessionJob, backref='sessions', cascade='all, delete')
    containers = relationship('Container', secondary=SessionContainer, backref='sessions', cascade='all, delete')
    files = relationship('File', secondary=SessionFile, backref='sessions', cascade='all, delete')

    def __init__(self, name='anonymous', **kwargs):
        super().__init__(name=name, **kwargs)       # Default session name

    def __repr__(self):
        if self.name == 'anonymous':
            return 'Session({0}: anonymous[{1}])'.format(self.pkid, str(self.accessed).split('.')[0])
        elif self.name is None:
            return 'Session({0}: {1})'.format(self.pkid, self.uid)
        else:
            return 'Session({0}: {1})'.format(self.pkid, self.name)


def cleanup_anon_sessions():
    '''
    Keep only the [5] (specified in :class:`~exa.config.Config`) most recent
    anonymous sessions.
    '''
    anons = session.query(Session).filter(
        Session.name == 'anonymous'
    ).order_by(Session.accessed).all()[:-Config.maxanonsessions]
    for anon in anons:
        session.delete(anon)
