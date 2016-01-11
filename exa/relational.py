# -*- coding: utf-8 -*-
'''
Dashboard, Container, and Relational Objects
===============================================
Definition of the content management system (CMS) and primary working
interfaces (graphical or terminal based).

Dashboard
----------------
Dedicated Python object for performing CMS actions

Container
-------------------
Data processing object used for manipulating data in memory as well as on
disk. Furthermore, this object has relationship information for CMS actions.
'''
from sqlalchemy import (Table, Column, Integer, String, DateTime, ForeignKey,
                        Float, create_engine, and_, event)
from datetime import datetime
from exa import Config
from exa import _pd as pd
from exa import _json as json
from exa.errors import MissingProgramError, MissingProjectError, MissingJobError
from exa.utils import gen_uid
if Config.ipynb:                  # If using Jupyter notebook
    from exa.widget import Widget

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




ProjectJob = Table(
    'projectjob',
    Base.metadata,
    Column('project_pkid', Integer, ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)
ProjectContainer = Table(
    'projectcontainer',
    Base.metadata,
    Column('project_pkid', Integer, ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)
ProjectFile = Table(
    'projectfile',
    Base.metadata,
    Column('project_pkid', Integer, ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)

ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)



class Program(Base):
    '''
    Long term or on-going project
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    projects = relationship('Project', secondary=ProgramProject, backref='programs', cascade='all, delete')
    jobs = relationship('Job', secondary=ProgramJob, backref='programs', cascade='all, delete')
    containers = relationship('Container', secondary=ProgramContainer, backref='programs', cascade='all, delete')
    files = relationship('File', secondary=ProgramFile, backref='programs', cascade='all, delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Dashboard._add_to_session(self)


class Project(Base):
    '''
    Carefully planned enterprise to achieve a specific aim.
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    jobs = relationship('Job', secondary=ProjectJob, backref='projects', cascade='all, delete')
    containers = relationship('Container', secondary=ProjectContainer, backref='projects', cascade='all, delete')
    files = relationship('File', secondary=ProjectFile, backref='projects', cascade='all, delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Dashboard._add_to_session(self)
        Dashboard._add_to_program(self)


class Job(Base):
    '''
    Specific task in a :class:`~exa.relational.Program` or
    :class:`~exa.relational.Project`.
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    containers = relationship('Container', secondary=JobContainer, backref='jobs', cascade='all, delete')
    files = relationship('File', secondary=JobFile, backref='jobs', cascade='all, delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Dashboard._add_to_session(self)
        Dashboard._add_to_program(self)
        Dashboard._add_to_project(self)


class File(Base):
    '''
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)
    ext = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    size = Column(Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Dashboard._add_to_session(self)
        Dashboard._add_to_program(self)
        Dashboard._add_to_project(self)
        Dashboard._add_to_job(self)





class Dashboard:
    '''
    '''
    _info = 'session: {0}\nprogram: {1}\nproject: {2}\njob: {3}\ncontainers: {4}'
    _load_object = {
        'session': lambda pkid: Session[pkid],
        'program': lambda pkid: Program[pkid],
        'project': lambda pkid: Project[pkid],
        'job': lambda pkid: Job[pkid]
    }

    def _add_to_session(self, obj):
        if isinstance(obj, Program):
            self._active_session.programs.append(obj)
        elif isinstance(obj, Project):
            self._active_session.projects.append(obj)
        elif isinstance(obj, Job):
            self._active_session.jobs.append(obj)
        elif isinstance(obj, Container):
            self._active_session.containers.append(obj)
        elif isinstance(obj, File):
            self._active_session.files.append(obj)
        else:
            raise TypeError('Unsupported type {0}'.format(type(obj)))

    def _add_to_program(self, obj):
        if self._active_program:
            if isinstance(obj, Project):
                self._active_program.projects.append(obj)
            elif isinstance(obj, Job):
                self._active_program.jobs.append(obj)
            elif isinstance(obj, Container):
                self._active_program.containers.append(obj)
            elif isinstance(obj, File):
                self._active_program.files.append(obj)
            else:
                raise TypeError('Unsupported type {0}'.format(type(obj)))
        else:
            pass
            #raise MissingProgramError()

    def _add_to_project(self, obj):
        if self._active_project:
            if isinstance(obj, Job):
                self._active_project.jobs.append(obj)
            elif isinstance(obj, Container):
                self._active_project.containers.append(obj)
            elif isinstance(obj, File):
                self._active_project.files.append(obj)
            else:
                raise TypeError('Unsupported type {0}'.format(type(obj)))
        else:
            pass
            #raise MissingProjectError()

    def _add_to_job(self, obj):
        if self._active_job:
            if isinstance(obj, Container):
                self._active_job.containers.append(obj)
            elif isinstance(obj, File):
                self._active_job.files.append(obj)
            else:
                raise TypeError('Unsupported type {0}'.format(type(obj)))
        else:
            pass
            #raise MissingJobError()

    @property
    def sessions(self):
        '''
        '''
        return Session.listall()

    @property
    def active(self):
        print(self._info.format(
            self._active_session,
            self._active_program,
            self._active_project,
            self._active_job,
            self._active_container
        ))

    def new_session(self, name='anonymous', description=None):
        '''
        Start a new session
        '''
        commit()
        self._active_session = Session(name=name, description=None)

    def import_session(self, key):
        raise NotImplementedError()

    def load_session(self, key):
        self._active_session = Session[key]

    def load_program(self, key):
        self._active_program = Program[key]

    def load_project(self, key):
        self._active_project = Project[key]

    def load_job(self, key):
        self._active_job = Job[key]

    def load_container(self, key):
        self._active_container = Container[key]

    def __init__(self, session, program, project, job, container):
        '''
        Load active session/program/project/job/container if defined in Config.
        '''
        self._active_session = Session[session] if session else Session(name='anonymous')
        self._active_program = Program[program] if program else None
        self._active_project = Project[project] if project else None
        self._active_job = Job[job] if job else None
        self._active_container = Container.load[container] if container else None
        self._widget = None
        if Config.ipynb:
            self._widget = Widget()

    def _repr_html_(self):
        self._widget._ipython_display_()

    def __repr__(self):
        return str(self.sessions)


Dashboard = Dashboard(*Config.session_args())
