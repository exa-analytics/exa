# -*- coding: utf-8 -*-
'''
Container
===============================================
Metadata is stored as json on disk
'''
from exa import _pd as pd
from exa import DataFrame
from exa.relational.base import session, datetime, relationship, event
from exa.relational.base import Column, Integer, String, DateTime
from exa.relational.base import ForeignKey, Table, Base
from exa.utils import gen_uid


ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Container(Base):
    '''
    Database representation of the 'session' concept.

    Warning:
        The correct way to set DataFrame object is as follows:

        .. code-block:: Python

            c = exa.Container()
            df = pd.DataFrame()
            c['name'] = df
            # or
            setattr(c, 'name', df)

        Avoid setting objects using the **__dict__** attribute as follows:

        .. code-block:: Python

            universe = atomic.Universe()
            c = exa.Container()
            df = pd.DataFrame()
            c.name = df

        (This is used in **__init__** where type control is enforced.)

    See Also:
        :class:`~exa.session.Session`
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    container_type = Column(String(16))
    size = Column(Integer)
    file_count = Column(Integer)
    files = relationship('File', secondary=ContainerFile, backref='containers', cascade='all, delete')
    __mapper_args__ = {
        'polymorphic_identity': 'container',   # This allows the container to
        'polymorphic_on': container_type,      # be inherited.
        'with_polymorphic': '*'
    }
    __dfclasses__ = {}

    def to_archive(self, path):
        '''
        Export this container to an archive that can be imported elsewhere.
        '''
        raise NotImplementedError()

    @classmethod
    def from_archive(cls, path):
        '''
        Import a container from an archive into the current active session.

        Note:
            This function will also create file entries and objects
            corresponding to the data provided in the archive.
        '''
        raise NotImplementedError()

    @property
    def dataframes(self):
        '''
        Return:
            dfs (dict): Dictionary of dataframes (key is the dataframe name)
        '''
        return {n: v for n, v in vars(self).items() if isinstance(v, pd.DataFrame)}

    def _dfcls(self, key):
        '''
        '''
        for k, v in self.__dfclasses__.items():
            if k == key:
                return v
        return DataFrame

    def __getitem__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        '''
        Check the value type and set :class:`~exa.dataframe.DataFrame` objects
        by casting them to the correct type.

        .. code-block:: Python

            container = exa.Container()
            print(container.__dftypes__)
            container.name = object
            type(container.name)
        '''
        print('here')
        if isinstance(value, pd.DataFrame):
            print('and here')
            value = self._dfcls(key)(value)
        setattr(self, key, value)

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __init__(self, name=None, description=None, dataframes={}, meta=None):
        super().__init__(name=name, description=description)
        for k, v in dataframes.items():
            setattr(self, k, v)
        self.meta = meta

    def __repr__(self):
        c = self.__class__.__name__
        p = self.pkid
        n = self.name
        u = self.uid
        return '{0}({1}: {2}[{3}])'.format(c, p, n, u)

    def __str__(self):
        return self.__repr__()


def concat(containers, axis=0, join='inner'):
    '''
    Concatenate a collection of containers.
    '''
    raise NotImplementedError()
