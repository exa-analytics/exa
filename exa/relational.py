# -*- coding: utf-8 -*-
'''
Relational Database Tables
==================================

Note
    All database interaction is lazy. Objects are commited when
    a users attempts to query the database and on exit.
'''
from sqlalchemy import (Table, Column, Integer, String, DateTime, ForeignKey,
                        Float, create_engine, and_)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from datetime import datetime
from exa import Config
from exa import _bz as bz
from exa.utils import gen_uid


@as_declarative()
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

    def df(cls):
        '''
        '''
        pass

    def __repr__(cls):
        return '{0}({1})'.format(cls.__class__.__name__, cls.pkid)


# Relationships are initialized in this manner because their Python
# class objects haven't yet been defined in the module.
RegisterFile = Table(
    'registerfile',
    Base.metadata,
    Column('register_pkid', Integer, ForeignKey('register.pkid')),
    Column('file_pkid', Integer, ForeignKey('file.pkid'))
)


RegisterProgram = Table(
    'registerprogram',
    Base.metadata,
    Column('register_pkid', Integer, ForeignKey('register.pkid')),
    Column('program_pkid', Integer, ForeignKey('program.pkid'))
)


RegisterProject = Table(
    'registerproject',
    Base.metadata,
    Column('register_pkid', Integer, ForeignKey('register.pkid')),
    Column('project_pkid', Integer, ForeignKey('project.pkid'))
)


RegisterJob = Table(
    'registerjob',
    Base.metadata,
    Column('register_pkid', Integer, ForeignKey('register.pkid')),
    Column('job_pkid', Integer, ForeignKey('job.pkid'))
)


RegisterContainer = Table(
    'registercontainer',
    Base.metadata,
    Column('register_pkid', Integer, ForeignKey('register.pkid')),
    Column('container_pkid', Integer, ForeignKey('container.pkid'))
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


class Register(Base):
    '''
    Database representation of the 'store' concept.

    See Also:
        :class:`~exa.store.Store`
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)


class Container(Base):
    '''
    Database representation of the 'store' concept.

    See Also:
        :class:`~exa.store.Store`
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)


class Program(Base):
    '''
    Long term or on-going project
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)


class Project(Base):
    '''
    Carefully planned enterprise to achieve a specific aim.
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)


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


class Isotope(Base):
    '''
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
        return 'Isotope({0}{1})'.format(self.A, self.symbol)

class Constant(Base):
    '''
    Physical constants.
    '''
    __tablename__ = 'constants'

    symbol = Column(String, nullable=False)
    value = Column(Float, nullable=False)


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


class Length(Base, Dimension):
    pass

class Mass(Base, Dimension):
    pass

class Time(Base, Dimension):
    pass

class Current(Base, Dimension):
    pass

class Temperature(Base, Dimension):
    pass

class Amount(Base, Dimension):
    pass

class Luminosity(Base, Dimension):
    pass

class Dose(Base, Dimension):
    pass

class Acceleration(Base, Dimension):
    '''
    Lt^-2 conversions.

    Parameters
        stdgrav: Standard gravity
    '''
    pass

class Angle(Base, Dimension):
    pass

class Charge(Base, Dimension):
    pass

class Dipole(Base, Dimension):
    '''
    Electric dipole moment.
    '''
    pass

class Energy(Base, Dimension):
    pass

class Force(Base, Dimension):
    pass

class Frequency(Base, Dimension):
    pass

class MolarMass(Base, Dimension):
    pass


engine_name = Config.relational_engine()
engine = create_engine(engine_name)
Base.metadata.create_all(engine)
db = bz.Data(engine)
