# -*- coding: utf-8 -*-
'''
Relational Database Support
==================================

Note
    All database interaction is lazy. Objects are commited when
    a users attempts to query the database and on exit.
'''
from sqlalchemy import (Table, Column, Integer, String, DateTime, ForeignKey,
                        Float, create_engine, and_)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from blaze import odo, Data
from datetime import datetime
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
    'projectjob,
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


class Program(Base):
    '''
    Long term or on-going project
    '''
    name - Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)


class Project(Base):
    '''
    Carefully planned enterprise to achieve a specific aim.
    '''
    name - Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)


class Job(Base):
    '''
    Specific task in a :class:`~exa.relational.Program` or
    :class:`~exa.relational.Project`.
    '''
    name - Column(String)
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


engine_name = 'sqlite://'
Engine = create_engine(engine_name)
Base.metadata.create_all(Engine)
DB = Data(Engine)







#import gc
#from uuid import uuid4
#from sqlalchemy import (Table, Column, Integer, String, DateTime, ForeignKey,
#                        Float, create_engine, and_)
#from sqlalchemy.orm import sessionmaker, relationship
#from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
#from IPython.display import display
#from itertools import product
#from exa import bz, pd, datetime, Config, get_logger, np, yaml, Loader, Dumper
#from exa.testers import UnitTester
#from exa.utils import mkpath
#
#
#_logger = get_logger('relational')
#
#
# Base classes
#class BaseTable:
#    '''
#    '''
#    # Columns common to all data tables
#    id = Column(Integer, primary_key=True)
#
#    @classmethod
#    def _bulk_save(cls, dataset):
#        '''
#        Performs a bulk insert into a specific table.
#
#        Args
#            cls: Table's class object instance (e.g. Isotope)
#            dataset: List of dictionary objects representing entries
#        '''
#        commit_all()
#        ENGINE.execute(cls.__table__.insert(), dataset)
#
#    def __repr__(self):
#        return '{0}({1}: \"{2}\")'.format(self.__class__.__name__, self.id, self.name)
#
#
#class BaseMeta(DeclarativeMeta):
#    '''
#    '''
#    # Public
#    def _items(self):
#        return self.__dict__.items()
#
#    def to_dict(self):
#        '''
#        Generate a dictionary representation of the relational object
#
#        Returns
#            d (dict): Dictionary of column name, column value pairs
#        '''
#        return dict([(k, v) for k, v in self._items() if isinstance(v, Column)])
#
#    def df(cls):
#        '''
#        Pull the relational table into a :class:`~pandas.DataFrame`.
#
#        Returns
#            df (:class:`~pandas.DataFrame`): Dataframe representation of the table
#
#        Warning
#            On large tables this operation can be very slow and/or cause a MemoryError.
#        '''
#        commit_all()    # Before any db IO we do a full commit
#        return bz.odo(DB[cls.__tablename__], pd.DataFrame).set_index('id')
#
#    def head(cls):
#        '''
#        '''
#        commit_all()
#        return cls.df().head()
#
#    def tail(cls):
#        '''
#        '''
#        commit_all()
#        return cls.df().tail()
#
#    def units(self):
#        obj = self.df()
#        if 'from_unit' in obj.columns:
#            print(obj['from_unit'].unique().tolist())
#        elif 'strid' in obj.columns:
#            print(obj['strid'].unique().tolist())
#        elif 'symbol' in obj.columns:
#            print(obj['symbol'].unique().tolist())
#
#    # Private
#    def _get_by_dict(cls, dict_key):
#        '''
#        '''
#        items = SESSION.query(cls)
#        for attr, value in key.items():
#            items = items.filter(getattr(cls, attr).like('%%%s%%' % value))
#        return items.all()
#
#    def _get_by_id(cls, key, id_='id'):
#        '''
#        '''
#        return SESSION.query(cls).filter(cls.__dict__[id_] == key).all()
#
#    def _get_by_ids(cls, keys, id_='id'):
#        '''
#        '''
#        return SESSION.query(cls).filter(cls.__dict__[id_].in_(tuple(keys)))
#
#    def _get_by_name(cls, key, name='name'):
#        '''
#        '''
#        return SESSION.query(cls).filter(cls.__dict__[name] == key).all()
#
#    def _get_by_names(cls, keys, name='name'):
#        '''
#        '''
#        return SESSION.query(cls).filter(cls.__dict__[name].in_(tuple(keys)))
#
#    def _get_factor(cls, _from, _to):
#        '''
#        '''
#        return SESSION.query(cls).filter(
#            and_(cls.from_unit == _from, cls.to_unit == _to)
#            ).all()[0].factor
#
#    def __getitem__(cls, key):
#        '''
#        Flexible getter that accepts integers, slices, strings, tuples,
#        and lists as arguments.
#        '''
#        commit_all()    # Before any db IO we do a full commit
#        # Based on the type of key we get in different ways
#        itemlist = None
#        first = False
#        if isinstance(key, dict):
#            first = True
#            itemlist = cls._get_by_dict(dict(key))
#        elif isinstance(key, int):
#            first = True
#            if cls.__tablename__ == 'isotopes':
#                itemlist = cls._get_by_id(key, id_='szuid')
#            else:
#                itemlist = cls._get_by_id(key)
#        elif isinstance(key, str):
#            first = True
#            if cls.__tablename__ == 'isotopes':
#                itemlist = cls._get_by_name(key, 'strid')
#            elif cls.__tablename__ == 'constants':
#                itemlist = cls._get_by_name(key, 'symbol')
#            else:
#                itemlist = cls._get_by_name(key)
#        elif isinstance(key, list) or isinstance(key, tuple):
#            full = True
#            if isinstance(key[0], int):
#                if cls.__tablename__ == 'isotopes':
#                    itemlist = cls._get_by_ids(key, id_='szuid')
#                else:
#                    itemlist = cls._get_by_ids(key)
#            elif isinstance(key[0], str):
#                if cls in Dimension.__subclasses__():
#                    itemlist = cls._get_factor(_from=key[0], _to=key[1])
#                else:
#                    if cls.__tablename__ == 'isotopes':
#                        itemlist = cls._get_by_names(key, 'strid')
#                    elif cls.__tablename__ == 'constants':
#                        itemlist = cls._get_by_names(key, 'symbol')
#                    else:
#                        itemlist = cls._get_by_names(key)
#            else:
#                raise TypeError('Unknown type for key ({0})'.format(type(key)))
#        else:
#            raise TypeError('Unknown type for key ({0})'.format(type(key)))
#        if first:
#            return itemlist[0]
#        else:
#            return itemlist
#
#
#BaseTable = declarative_base(cls=BaseTable, metaclass=BaseMeta)
#
#
# Relationship tables
#projects_jobs = Table('projects_jobs', BaseTable.metadata,
#                      Column('project_id', Integer, ForeignKey('projects.id')),
#                      Column('job_id', Integer, ForeignKey('jobs.id')))
#
#
#projects_files = Table('projects_files', BaseTable.metadata,
#                       Column('project_id', Integer, ForeignKey('projects.id')),
#                       Column('file_id', Integer, ForeignKey('files.id')))
#
#
#jobs_files = Table('jobs_files', BaseTable.metadata,
#                   Column('job_id', Integer, ForeignKey('jobs.id')),
#                   Column('file_id', Integer, ForeignKey('files.id')))
#
#
# Tables
#class Project(BaseTable):
#    '''
#    '''
#    __tablename__ = 'projects'
#
#    name = Column(String(128), unique=True, nullable=False)
#    jobs = relationship('Job', secondary=projects_jobs, backref='projects')
#    files = relationship('File', secondary=projects_files, backref='projects')
#    description = Column(String, nullable=True)
#    created = Column(DateTime, default=datetime.now)
#
#    @property
#    def files_table(self):
#        '''
#        '''
#        # THIS NEEDS A REWORK. IT IS A SQL JOIN NOT AN UGLY HACK
#        project_files = [f.id for f in self.files]
#        jobs_files = [f.id for job in self.jobs for f in job.files]
#        pfiles = bz.odo(DB.files[DB.files.id.isin(project_files)], pd.DataFrame).set_index('id')
#        jfiles = bz.odo(DB.files[DB.files.id.isin(jobs_files)], pd.DataFrame).set_index('id')
#        jids = bz.odo(DB.jobs_files, pd.DataFrame)
#        jids = jids.loc[jids.file_id.isin(jobs_files)].set_index('file_id')
#        jids.index.names = ['id']
#        all_files = pd.concat((pfiles, jfiles))
#        joined = pd.concat((jids, all_files), axis=1).sort_values('job_id', na_position='first')
#        joined.index.names = ['file_id']
#        return joined
#
#
#class Job(BaseTable):
#    '''
#    '''
#    __tablename__ = 'jobs'
#
#    name = Column(String(128))
#    files = relationship('File', secondary=jobs_files, backref='jobs')
#    created = Column(DateTime, default=datetime.now)
#    description = Column(String, nullable=True)
#
#    @property
#    def files_table(self):
#        '''
#        '''
#        file_ids = [f.id for f in self.files]
#        files = bz.odo(DB.files[DB.files.id.isin(file_ids)], pd.DataFrame).set_index('id')
#        return files
#
#
#class File(BaseTable):
#    '''
#    A representation of a file object. A number of the attributes are set automatically: the user
#    does not need to set any values explicity.
#
#    Attributes
#        id (int): Internal id
#        uid (str): Identifier on disk
#        created (datetime): Datetime stamp of creation
#        name (str): File name (optional)
#        description (str): File description (optional)
#        ftype (str): File type (optional)
#        size (int): File size (in megabytes)
#    '''
#    __tablename__ = 'files'
#
#    name = Column(String(128), unique=False, nullable=True)
#    description = Column(String, nullable=True)
#    uid = Column(String(32))
#    created = Column(DateTime, default=datetime.now)
#    ftype = Column(String, nullable=False)
#    size = Column(Integer, nullable=True)
#
#    @classmethod
#    def _get_by_uid(cls, uid):
#        '''
#        Get all files with the given uid.
#        '''
#        return SESSION.query(cls).filter(cls.uid == uid).all()
#
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        self.uid = uuid4().hex
#
#
#class Isotope(BaseTable):
#    '''
#    Isotope data.
#    '''
#    __tablename__ = 'isotopes'
#
#    A = Column(Integer, nullable=False)
#    Z = Column(Integer, nullable=False)
#    af = Column(Float)
#    eaf = Column(Float)
#    color = Column(Integer)
#    radius = Column(Float)
#    gfactor = Column(Float)
#    mass = Column(Float)
#    emass = Column(Float)
#    name = Column(String(length=16))
#    eneg = Column(Float)
#    quadmom = Column(Float)
#    spin = Column(Float)
#    symbol = Column(String(length=3))
#    szuid = Column(Integer)
#    strid = Column(Integer)
#
#    def __repr__(self):
#        return 'Isotope({0}{1})'.format(self.A, self.symbol)
#
#
#class Constant(BaseTable):
#    '''
#    Physical constants.
#    '''
#    __tablename__ = 'constants'
#
#    symbol = Column(String, nullable=False)
#    value = Column(Float, nullable=False)
#
#
#class Dimension:
#    '''
#    Generic class for physical dimension conversions. Doesn't do anything
#    by itself but is inherited by specific dimension classes.
#
#    Attributes
#        from_unit (str): Unit to convert from
#        to_unit (str): Unit to convert to
#        factor (float): Conversion factor
#
#    Methods
#        units: Displays a list of possible units
#
#    See Also
#        :class:`~exa.relational.Length`
#    '''
#    from_unit = Column(String(8), nullable=False)
#    to_unit = Column(String(8), nullable=False)
#    factor = Column(Float, nullable=False)
#
#
#class Length(BaseTable, Dimension):
#    __tablename__ = 'length'
#
#
#class Mass(BaseTable, Dimension):
#    __tablename__ = 'mass'
#
#
#class Time(BaseTable, Dimension):
#    __tablename__ = 'time'
#
#
#class Current(BaseTable, Dimension):
#    __tablename__ = 'current'
#
#
#class Temperature(BaseTable, Dimension):
#    __tablename__ = 'temperature'
#
#
#class Amount(BaseTable, Dimension):
#    __tablename__ = 'amount'
#
#
#class Luminosity(BaseTable, Dimension):
#    __tablename__ = 'luminosity'
#
#
#class Dose(BaseTable, Dimension):
#    __tablename__ = 'dose'
#
#
#class Acceleration(BaseTable, Dimension):
#    '''
#    Lt^-2 conversions.
#
#    Parameters
#        stdgrav: Standard gravity
#    '''
#    __tablename__ = 'acceleration'
#
#
#class Angle(BaseTable, Dimension):
#    __tablename__ = 'angle'
#
#
#class Charge(BaseTable, Dimension):
#    __tablename__ = 'charge'
#
#
#class Dipole(BaseTable, Dimension):
#    '''
#    Electric dipole moment.
#    '''
#    __tablename__ = 'dipole'
#
#
#class Energy(BaseTable, Dimension):
#    __tablename__ = 'energy'
#
#
#class Force(BaseTable, Dimension):
#    __tablename__ = 'force'
#
#
#class Frequency(BaseTable, Dimension):
#    __tablename__ = 'frequency'
#
#
#class MolarMass(BaseTable, Dimension):
#    __tablename__ = 'molarmass'
#
#
# Globals and table creation!
# TODO: This will need to get changed to support PostgreSQL
#ENGINE_NAME = '{0}:///{1}/{2}'.format(Config.relational['backend'],
#                                      Config.exa,
#                                      Config.relational['database'])
#ENGINE = create_engine(ENGINE_NAME)
#BaseTable.metadata.create_all(ENGINE)     # TABLE CREATED HERE!!!
#SESSIONMAKER = sessionmaker(bind=ENGINE, autoflush=True)
#SESSION = SESSIONMAKER()
#DB = bz.Data(ENGINE)
#
#
# Functions
#def get_active_objects():
#    '''
#    '''
#    objs = []
#    for obj in gc.get_objects():
#        if isinstance(obj, BaseTable):
#            objs.append(obj)
#    return objs
#
#
#def commit_all():
#    '''
#    Commit all (relational) objects in memory to the database.
#    '''
#    for obj in get_active_objects():
#        if obj.id is None:
#            SESSION.add(obj)
#    try:
#        SESSION.commit()
#    except Exception as e:
#        SESSION.rollback()
#        _logger.error(str(e))
#        commit_one_at_a_time()
#
#
#def commit_one_at_a_time():
#    '''
#    '''
#    for obj in gc.get_objects():
#        if isinstance(obj, BaseTable):
#            if obj.id is None:
#                try:
#                    SESSION.add(obj)
#                    SESSION.commit()
#                except:
#                    SESSION.rollback()
#
#def end_session():
#    '''
#    Cleanup open comms to databases prior to exiting.
#    '''
#    commit_all()
#    SESSION.close_all()
#
#
# Test engine
#_ENGINE_NAME = '{0}:///{1}/{2}'.format(Config.relational['backend'],
#                                       Config.exa,
#                                       Config.relational['database'])
#_ENGINE = create_engine(_ENGINE_NAME)
#BaseTable.metadata.create_all(_ENGINE)     # TABLE CREATED HERE!!!
#_SESSIONMAKER = sessionmaker(bind=_ENGINE, autoflush=True)
#_SESSION = _SESSIONMAKER()
#_DB = bz.Data(_ENGINE)
#
#
## Check if we need to load data in to the database!
# TODO: This logic can be improved to perform disk io only twice
#for tbl in Dimension.__subclasses__() + [Isotope, Constant]:
#    count = 0
#    try:
#        count = DB[tbl.__tablename__].count()
#    except:
#        pass
#    if count == 0:
#        print('Loading {0} data'.format(tbl.__tablename__))
#        data = None
#        if tbl.__tablename__ == 'isotopes':
#            with open(mkpath(Config.static, 'isotopes.yml')) as f:
#                data = yaml.load(f, Loader=Loader)
#            data = list(data.values())
#        elif tbl.__tablename__ == 'constants':
#            with open(mkpath(Config.static, 'constants.yml')) as f:
#                data = yaml.load(f, Loader=Loader)['constants']
#            data = list({'symbol': key, 'value': value} for key, value in data.items())
#        else:
#            with open(mkpath(Config.static, 'units.yml')) as f:
#                data = yaml.load(f, Loader=Loader)[tbl.__tablename__]
#            labels = list(data.keys())
#            values = np.array(list(data.values()))
#            cols = list(product(labels, labels))
#            values_t = values.reshape(len(values), 1)
#            l = (values / values_t).ravel()
#            data = [{'from_unit': cols[i][0], 'to_unit': cols[i][1], 'factor': l[i]} for i in range(len(l))]
#        tbl._bulk_save(data)
#
#
# Updated database engines
#DB = bz.Data(ENGINE)
#_DB = bz.Data(_ENGINE)
#
