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
    _info = 'session: {0}\nprogram: {1}\nproject: {2}\njob: {3}\ncontainers: {4}'
    _load_object = {
        'session': lambda pkid: Session[pkid],
        'program': lambda pkid: Program[pkid],
        'project': lambda pkid: Project[pkid],
        'job': lambda pkid: Job[pkid]
    }

    @staticmethod
    @event.listens_for(mapper, 'init')
    def _add_to_relational_session(obj, args, kwargs):
        print('autoadd')
        print(obj)
        print(args)
        print(kwargs)

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

    #def _repr_html_(self):
    #    self._widget._ipython_display_()

    def __repr__(self):
        return str(self.sessions)


Dashboard = Dashboard(*Config.session_args())
