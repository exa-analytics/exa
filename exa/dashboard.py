# -*- coding: utf-8 -*-
'''
Dashboard
==============
'''
from exa import Config
from exa.relational import Session, Program, Project, Job, Container, File
from exa.relational.base import event, session, mapper
if Config.ipynb:                  # If using Jupyter notebook
    from exa.widget import Widget

class Dashboard:
    '''
    '''
    def _add_object_relations(self, obj):
        '''
        '''
        session_appenders = {
            'program': lambda: self._active_session.programs.append(obj),
            'project': lambda: self._active_session.projects.append(obj),
            'job': lambda: self._active_session.jobs.append(obj),
            'container': lambda: self._active_session.containers.append(obj),
            'file': lambda: self._active_session.files.append(obj)
        }
        program_appenders = {
            'project': lambda: self._active_program.projects.append(obj),
            'job': lambda: self._active_program.jobs.append(obj),
            'container': lambda: self._active_program.containers.append(obj),
            'file': lambda: self._active_program.files.append(obj)
        }
        project_appenders = {
            'job': lambda: self._active_project.jobs.append(obj),
            'container': lambda: self._active_project.containers.append(obj),
            'file': lambda: self._active_project.files.append(obj)
        }
        job_appenders = {
            'container': lambda: self._active_job.containers.append(obj),
            'file': lambda: self._active_job.files.append(obj)
        }
        container_appenders = {
            'file': lambda: self._active_container.files.append(obj)
        }
        tbl = obj.__tablename__
        if self._active_session:
            session_appenders[tbl]()
        if self._active_program:
            program_appenders[tbl]()
        if self._active_project:
            project_appenders[tbl]()
        if self._active_job:
            job_appenders[tbl]()
        if self._active_container:
            container_appenders[tbl]()

    def __init__(self):
        '''
        Load active session/program/project/job/container if defined in Config.
        '''
        self._active_session = None
        self._active_program = None
        self._active_project = None
        self._active_job = None
        self._active_container = None
        self._widget = None
        if Config.ipynb:
            self._widget = Widget()

    def _init(self, session, program, project, job, container):
        self._active_session = Session[session] if session else Session(name='anonymous')
        self._active_program = Program[program] if program else None
        self._active_project = Project[project] if project else None
        self._active_job = Job[job] if job else None
        self._active_container = Container[container] if container else None

    def __repr__(self):
        return str(self.sessions)


@event.listens_for(mapper, 'init')
def add_to_db_session(obj, args, kwargs):
    '''
    All relational objects are automatically added to the database session.
    These objects' relations are also automatically instantiated here.

    See Also:
        :mod:`~exa.relational.base`
    '''
    session.add(obj)
    Dashboard._add_object_relations(obj)



Dashboard = Dashboard()
Dashboard._init(*Config.session_args())


#    _info = 'session: {0}\nprogram: {1}\nproject: {2}\njob: {3}\ncontainers: {4}'
#    _load_object = {
#        'session': lambda pkid: Session[pkid],
#        'program': lambda pkid: Program[pkid],
#        'project': lambda pkid: Project[pkid],
#        'job': lambda pkid: Job[pkid]
#    }
#
#    def _add_to_session(self, obj):
#        if isinstance(obj, Program):
#            self._active_session.programs.append(obj)
#        elif isinstance(obj, Project):
#            self._active_session.projects.append(obj)
#        elif isinstance(obj, Job):
#            self._active_session.jobs.append(obj)
#        elif isinstance(obj, Container):
#            self._active_session.containers.append(obj)
#        elif isinstance(obj, File):
#            self._active_session.files.append(obj)
#        else:
#            raise TypeError('Unsupported type {0}'.format(type(obj)))
#
#    def _add_to_program(self, obj):
#        if self._active_program:
#            if isinstance(obj, Project):
#                self._active_program.projects.append(obj)
#            elif isinstance(obj, Job):
#                self._active_program.jobs.append(obj)
#            elif isinstance(obj, Container):
#                self._active_program.containers.append(obj)
#            elif isinstance(obj, File):
#                self._active_program.files.append(obj)
#            else:
#                raise TypeError('Unsupported type {0}'.format(type(obj)))
#        else:
#            pass
#            #raise MissingProgramError()
#
#    def _add_to_project(self, obj):
#        if self._active_project:
#            if isinstance(obj, Job):
#                self._active_project.jobs.append(obj)
#            elif isinstance(obj, Container):
#                self._active_project.containers.append(obj)
#            elif isinstance(obj, File):
#                self._active_project.files.append(obj)
#            else:
#                raise TypeError('Unsupported type {0}'.format(type(obj)))
#        else:
#            pass
#            #raise MissingProjectError()
#
#    def _add_to_job(self, obj):
#        if self._active_job:
#            if isinstance(obj, Container):
#                self._active_job.containers.append(obj)
#            elif isinstance(obj, File):
#                self._active_job.files.append(obj)
#            else:
#                raise TypeError('Unsupported type {0}'.format(type(obj)))
#        else:
#            pass
#            #raise MissingJobError()
#
#    @property
#    def sessions(self):
#        '''
#        '''
#        return Session.listall()
#
#    @property
#    def active(self):
#        print(self._info.format(
#            self._active_session,
#            self._active_program,
#            self._active_project,
#            self._active_job,
#            self._active_container
#        ))
#
#    def new_session(self, name='anonymous', description=None):
#        '''
#        Start a new session
#        '''
#        commit()
#        self._active_session = Session(name=name, description=None)
#
#    def import_session(self, key):
#        raise NotImplementedError()
#
#    def load_session(self, key):
#        self._active_session = Session[key]
#
#    def load_program(self, key):
#        self._active_program = Program[key]
#
#    def load_project(self, key):
#        self._active_project = Project[key]
#
#    def load_job(self, key):
#        self._active_job = Job[key]
#
#    def load_container(self, key):
#        self._active_container = Container[key]
#
#    def __init__(self, session, program, project, job, container):
#        '''
#        Load active session/program/project/job/container if defined in Config.
#        '''
#        self._active_session = Session[session] if session else Session(name='anonymous')
#        self._active_program = Program[program] if program else None
#        self._active_project = Project[project] if project else None
#        self._active_job = Job[job] if job else None
#        self._active_container = Container.load[container] if container else None
#        self._widget = None
#        if Config.ipynb:
#            self._widget = Widget()
#
#    #def _repr_html_(self):
#    #    self._widget._ipython_display_()
#
#
