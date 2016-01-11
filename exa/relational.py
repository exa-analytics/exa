# -*- coding: utf-8 -*-
'''
Relational Database Tables
==================================
Database logic for the content management system.

Note:
    All database interaction is lazy. Objects are commited when
    a users attempts to query the database and on exit.
'''
from sqlalchemy import (Table, Column, Integer, String, DateTime, ForeignKey,
                        Float, create_engine, and_, event)
from sqlalchemy.orm import sessionmaker, scoped_session, mapper, relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from datetime import datetime
from operator import itemgetter
from exa import Config
from exa import _bz as bz
from exa import _pd as pd
from exa import _json as json
from exa.errors import MissingProgramError, MissingProjectError, MissingJobError
from exa.utils import gen_uid
if Config.interactive:
    from exa.widget import Widget


class Meta(DeclarativeMeta):
    '''
    Extends the default sqlalchemy table metaclass to allow for getting.
    '''

    def df(self):
        '''
        Display a :py:class:`~pandas.DataFrame` representation of the table.
        '''
        commit()
        df = bz.odo(db[self.__tablename__], pd.DataFrame)
        if 'pkid' in df.columns:
            return df.set_index('pkid')
        else:
            return df

    def listall(self):
        '''
        '''
        commit()
        return session.query(self).all()

    def _getitem(self, key):
        '''
        '''
        if isinstance(key, int):
            return session.query(self).filter(self.pkid == key).all()[0]
        else:
            raise NotImplementedError('Lookup by pkid only.')

    def __getitem__(self, key):
        commit()
        return self._getitem(key)


@as_declarative(metaclass=Meta)
class Base:
    '''
    Declarative base class (used by SQLAlchemy) to initialize relational tables.
    '''
    # Common keys
    pkid = Column(Integer, primary_key=True)

    # By default the table name is the lowercase class name
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def _bulk_insert(cls, data):
        '''
        Perform a bulk insert into a specific table.

        Args:
            data (list): List of dictionary objects representing rows
        '''
        commit()
        session.bulk_insert_mappings(cls, data)

    def __repr__(cls):
        return '{0}({1})'.format(cls.__class__.__name__, cls.pkid)


@event.listens_for(mapper, 'init')
def auto_add(target, args, kwargs):
    '''
    Automatically add newly created objects to the current database session.
    '''
    session.add(target)


def commit():
    '''
    Commit all of the objects currently in the session.
    '''
    try:
        session.commit()
    except:
        session.rollback()
        raise


def _cleanup_anon_sessions():
    '''
    Keep only the n most recently accessed anonymous sessions.
    '''
    anons = session.query(Session).filter(
        Session.name == 'anonymous'
    ).order_by(Session.accessed).all()[:-5]
    for anon in anons:
        session.delete(anon)
    commit()


SessionProgram = Table(
    'sessionprogram',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid')),
    Column('program_pkid', Integer, ForeignKey('program.pkid'))
)
SessionProject = Table(
    'sessionproject',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid')),
    Column('project_pkid', Integer, ForeignKey('project.pkid'))
)
SessionJob = Table(
    'sessionjob',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid')),
    Column('job_pkid', Integer, ForeignKey('job.pkid'))
)
SessionContainer = Table(
    'sessioncontainer',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid')),
    Column('container_pkid', Integer, ForeignKey('container.pkid'))
)
SessionFile = Table(
    'sessionfile',
    Base.metadata,
    Column('session_pkid', Integer, ForeignKey('session.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


ProgramProject = Table(
    'programproject',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid')),
    Column('project_pkid', Integer, ForeignKey('project.pkid'))
)
ProgramJob = Table(
    'programjob',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid')),
    Column('job_pkid', Integer, ForeignKey('job.pkid'))
)
ProgramContainer = Table(
    'programcontainer',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid')),
    Column('container_pkid', Integer, ForeignKey('container.pkid'))
)
ProgramFile = Table(
    'programfile',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid')),
    Column('file_pkid', Integer, ForeignKey('file.pkid'))
)


ProjectJob = Table(
    'projectjob',
    Base.metadata,
    Column('project_pkid', Integer, ForeignKey('project.pkid')),
    Column('job_pkid', Integer, ForeignKey('job.pkid'))
)
ProjectContainer = Table(
    'projectcontainer',
    Base.metadata,
    Column('project_pkid', Integer, ForeignKey('project.pkid')),
    Column('container_pkid', Integer, ForeignKey('container.pkid'))
)
ProjectFile = Table(
    'projectfile',
    Base.metadata,
    Column('project_pkid', Integer, ForeignKey('project.pkid')),
    Column('file_pkid', Integer, ForeignKey('file.pkid'))
)


JobContainer = Table(
    'jobcontainer',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid')),
    Column('container_pkid', Integer, ForeignKey('container.pkid'))
)
JobFile = Table(
    'jobfile',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid')),
    Column('file_pkid', Integer, ForeignKey('file.pkid'))
)
ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid')),
    Column('file_pkid', Integer, ForeignKey('file.pkid'))
)


class SessionMeta(Meta):
    '''
    '''
    def _getitem(self, key):
        if isinstance(key, int):
            return session.query(self).filter(self.pkid == key).all()[0]
        elif isinstance(key, str):
            return session.query(self).filter(self.name == key).all()[0]
        else:
            raise NotImplementedError()

class Session(Base, metaclass=SessionMeta):
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
    programs = relationship('Program', secondary=SessionProgram, backref='session', cascade='all, delete')
    projects = relationship('Project', secondary=SessionProject, backref='session', cascade='all, delete')
    jobs = relationship('Job', secondary=SessionJob, backref='session', cascade='all, delete')
    containers = relationship('Container', secondary=SessionContainer, backref='session', cascade='all, delete')
    files = relationship('File', secondary=SessionFile, backref='session', cascade='all, delete')

    def __repr__(self):
        if self.name == 'anonymous':
            return 'Session(anon: {0})'.format(str(self.accessed).split('.')[0])
        elif self.name is None:
            return 'Session({0})'.format(self.uid)
        else:
            return 'Session({0})'.format(self.name)


class Program(Base):
    '''
    Long term or on-going project
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    projects = relationship('Project', secondary=ProgramProject, backref='program', cascade='all, delete')
    jobs = relationship('Job', secondary=ProgramJob, backref='program', cascade='all, delete')
    containers = relationship('Container', secondary=ProgramContainer, backref='program', cascade='all, delete')
    files = relationship('File', secondary=ProgramFile, backref='program', cascade='all, delete')

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
    jobs = relationship('Job', secondary=ProjectJob, backref='project', cascade='all, delete')
    containers = relationship('Container', secondary=ProjectContainer, backref='project', cascade='all, delete')
    files = relationship('File', secondary=ProjectFile, backref='project', cascade='all, delete')

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
    containers = relationship('Container', secondary=JobContainer, backref='job', cascade='all, delete')
    files = relationship('File', secondary=JobFile, backref='job', cascade='all, delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Dashboard._add_to_session(self)
        Dashboard._add_to_program(self)
        Dashboard._add_to_project(self)


class Container(Base):
    '''
    Database representation of the 'session' concept.

    See Also:
        :class:`~exa.session.Session`
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)
    files = relationship('File', secondary=ContainerFile, backref='container', cascade='all, delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Dashboard._add_to_session(self)
        Dashboard._add_to_program(self)
        Dashboard._add_to_project(self)
        Dashboard._add_to_job(self)

    def __repr__(self):
        if self.name is None:
            return 'Container({0})'.format(self.uid)
        else:
            return 'Container({0})'.format(self.name)


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


class IsotopeMeta(Meta):
    '''
    '''
    def get_by_symbol(self, symbol):
        '''
        '''
        commit()
        return session.query(self).filter(self.symbol == symbol).all()

    def get_by_strid(self, element):
        '''
        '''
        commit()
        return session.query(self).filter(self.strid == element).all()[0]

    def get_szuid(self, number):
        '''
        '''
        commit()
        return session.query(self).filter(self.szuid == number).all()[0]

    def get_element(self, key, by='symbol'):
        '''
        Args:
            by (str): One of 'symbol' or 'znum' or 'asym'
            key: Symbol or proton number (znum) or 'ASymbol' (1H, 12C, etc)
        '''
        commit()
        if by == 'symbol':
            return session.query(self).filter(self.symbol == key).order_by(self.af).all()[-1]
        elif by == 'znum':
            return session.query(self).filter(self.Z == key).order_by(self.af).all()[-1]
        elif by == 'asym':
            return session.query(self).filter(self.strid == key).all()[-1]
        else:
            raise NotImplementedError()

    def get_elements(self, keys, by='symbol'):
        '''
        '''
        commit()
        return [self.get_element(key, by=by) for key in keys]

    def _getitem(self, key):
        commit()
        if isinstance(key, str):
            if key[0].isdigit():
                return self.get_by_strid(key)
            else:
                return self.get_by_symbol(key)
        elif isinstance(key, int):
            return self.get_by_szuid(key)
        else:
            raise TypeError('Key type {0} not supported.'.format(type(key)))


class Isotope(Base, metaclass=IsotopeMeta):
    '''
    A variant of a chemical element with a specific proton and neutron count.
    '''
    A = Column(Integer, nullable=False)
    Z = Column(Integer, nullable=False)
    af = Column(Float)
    eaf = Column(Float)
    color = Column(Integer)
    radius = Column(Float)
    gfactor = Column(Float)
    mass = Column(Float)
    emass = Column(Float)
    name = Column(String(length=16))
    eneg = Column(Float)
    quadmom = Column(Float)
    spin = Column(Float)
    symbol = Column(String(length=3))
    szuid = Column(Integer)
    strid = Column(Integer)

    def __repr__(self):
        return '{0}{1}'.format(self.A, self.symbol)


class Constant(Base):
    '''
    Physical constants.
    '''
    __tablename__ = 'constants'

    symbol = Column(String, nullable=False)
    value = Column(Float, nullable=False)


class DimensionMeta(Meta):
    '''
    '''
    def _getitem(self, key):
        commit()
        if isinstance(key, tuple):
            return self.get_factor(key)

    def get_factor(self, key):
        commit()
        f = key[0]
        t = key[1]
        return session.query(self).filter(and_(
            self.from_unit == f,
            self.to_unit == t
        )).all()[0].factor


class Dimension:
    '''
    Generic class for physical dimension conversions. Doesn't do anything
    by itself but is inherited by specific dimension classes.

    Attributes
        from_unit (str): Unit to convert from
        to_unit (str): Unit to convert to
        factor (float): Conversion factor

    Methods
        units: Displays a list of possible units

    See Also
        :class:`~exa.relational.Length`
    '''
    from_unit = Column(String(8), nullable=False)
    to_unit = Column(String(8), nullable=False)
    factor = Column(Float, nullable=False)


class Length(Base, Dimension, metaclass=DimensionMeta):
    pass
class Mass(Base, Dimension, metaclass=DimensionMeta):
    pass
class Time(Base, Dimension, metaclass=DimensionMeta):
    pass
class Current(Base, Dimension, metaclass=DimensionMeta):
    pass
class Temperature(Base, Dimension, metaclass=DimensionMeta):
    pass
class Amount(Base, Dimension, metaclass=DimensionMeta):
    pass
class Luminosity(Base, Dimension, metaclass=DimensionMeta):
    pass
class Dose(Base, Dimension, metaclass=DimensionMeta):
    pass
class Acceleration(Base, Dimension, metaclass=DimensionMeta):
    pass
class Angle(Base, Dimension, metaclass=DimensionMeta):
    pass
class Charge(Base, Dimension, metaclass=DimensionMeta):
    pass
class Dipole(Base, Dimension, metaclass=DimensionMeta):
    pass
class Energy(Base, Dimension, metaclass=DimensionMeta):
    pass
class Force(Base, Dimension, metaclass=DimensionMeta):
    pass
class Frequency(Base, Dimension, metaclass=DimensionMeta):
    pass
class MolarMass(Base, Dimension, metaclass=DimensionMeta):
    pass


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
            self._active_program = obj
        elif isinstance(obj, Project):
            self._active_session.projects.append(obj)
            self._active_project = obj
        elif isinstance(obj, Job):
            self._active_session.jobs.append(obj)
            self._active_job = obj
        elif isinstance(obj, Container):
            self._active_session.containers.append(obj)
            self._containers.append(obj)
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

    def sessions(self):
        '''
        '''
        return Session.listall()

    @property
    def info(self):
        print(self._info.format(
            self._active_session,
            self._active_program,
            self._active_project,
            self._active_job,
            self._containers
        ))

    def new_session(self, name='anonymous', description=None):
        '''
        '''
        self._active_session = Session(name=name, description=None)

    def load_session(self, key):
        self._active_session = Session.load(key)

    def __init__(self):
        self._active_session = None
        self._active_program = None
        self._active_project = None
        self._active_job = None
        self._containers = []
        self._widget = None
        if Config.interactive:
            self._widget = Widget()

    def _create_new(self, items):
        for k, v in items:
            name = '_active_' + k
            if v:
                setattr(self, name, self._load_object[k](v))
            elif k == 'session':
                setattr(self, name, Session(name='anonymous'))

    def _repr_html_(self):
        return self._widget

    def __repr__(self):
        return str(self.sessions())


engine_name = Config.relational_engine()
engine = create_engine(engine_name)
session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)
db = bz.Data(engine)
Dashboard = Dashboard()
Dashboard._create_new(Config.session)
