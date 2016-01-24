# -*- coding: utf-8 -*-
'''
Base Relational Objects
===============================================
This module outlines the event-based content management system established by exa and creates
a complex base table (schema) class, :class:`~exa.relational.base.Base`. The schema base class's
metaclass inherits the metaclass of :py:class:`~ipywidgets.DOMWidget` in order for certain
tables to be able to have HTML representations (within the `Jupyter notebook`_).

.. _Jupyter notebook: http://jupyter.org/
'''
from uuid import UUID
from datetime import datetime
from traitlets import MetaHasTraits
from sqlalchemy import Column, Integer, String, DateTime, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa import Config
from exa import _pd as pd
from exa.utils import gen_uid


class Meta(MetaHasTraits, DeclarativeMeta):
    '''
    Metaclass for relational objects that allows certain relational objects
    to act not only as a relational table schema and table entry, via
    `sqlalchemy`_, but also as a `Jupyter notebook`_ `widget`_.

    Tip:
        Combination of the metaclasses (like this) is required because the
        metaclass of a derived class must be a subclass of the metaclasses of
        all of its bases. As an example,

        .. code-block:: Python

            class Meta:
                pass

            class Klass(object, metaclass=Meta):
                pass

        doesn't work because the metaclass (Meta) is not a subclass of "object"'s
        metaclass (type).

        .. code-block:: Python

            class Meta(type):
                pass

            class Klass(object, metaclass=Meta):
                pass

        Now that the custom metaclass (Meta) has subclassed the metaclass of
        object, the Klass class object can be created.

    .. _sqlalchemy: http://www.sqlalchemy.org/
    .. _Jupyter notebook: http://jupyter.org/
    .. _widget: https://ipywidgets.readthedocs.org/en/latest/
    '''
    def __len__(self):                         # Length of the table (in database)
        return db_sess.query(self).count()

    def __iter__(self):                        # Iterate over every entry in the database
        for item in db_sess.query(self).all():
            yield item

    def __getitem__(self, key):
        '''
        This is called when a user attempts to slice/select an entry from the
        database table (the metaclass of the object is a representation of the
        table). This is not the getitem function that is called when a user
        attempts to slice an entry instance.

        .. code-block:: Python

            c = exa.Container[1]    # Loads the container with pkid == 1 (via this __getitem__)
            c[1]      # Slices the first (multiindex) level of each dataframe attached to this
            c[::4]    # container (via the :class:`~exa.relational.container.Container`'s __getitem__)

        '''
        if isinstance(key, int):
            return db_sess.query(self).filter(self.pkid == key).one()
        elif isinstance(key, str) and hasattr(self, 'name'):
            return db_sess.query(self).filter(self.name == key).one()
        elif isinstance(key, UUID) and hasattr(self, 'uid'):
            return db_sess.query(self).filter(self.uid == key.hex).one()
        elif hasattr(self, '_getitem'):
            return self._getitem(key)    # Allows for custom getters specific to certain classes
        else:
            raise KeyError('Unknown key {0}.'.format(key))


@as_declarative(metaclass=Meta)
class Base:
    '''
    Declarative base class (used by SQLAlchemy) to initialize relational tables.
    '''
    pkid = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def bulk_insert(cls, data):
        '''
        Perform a bulk insert into a specific table.

        .. code-block:: Python

            [{'column1': 'foo', 'column2': 42, 'column3': 'bar'}]

        Args:
            data (list): List of dictionary objects (mappings - see the example above)
        '''
        try:
            db_sess.bulk_insert_mappings(cls, data)
        except:
            db_sess.rollback()
            raise

    @classmethod
    def table(cls):
        '''
        Display a :py:class:`~pandas.DataFrame` representation of the table.

        Returns:
            df (:py:class:`~pandas.DataFrame`): In memory table copy
        '''
        df = pd.read_sql(db_sess.query(cls).statement, engine.connect())
        if 'pkid' in df.columns:
            return df.set_index('pkid')
        else:
            return df

    def __repr__(cls):
        return '{0}({1})'.format(cls.__class__.__name__, cls.pkid)


class Name:
    '''
    '''
    name = Column(String)
    description = Column(String)


class HexUID:
    '''
    Mixin when a unique ID is required.
    '''
    hexuid = Column(String(32), default=gen_uid)

    @property
    def uid(self):
        return UUID(self.hexuid)


class Time:
    '''
    Mixin for when date and time stamps for created, accessed, and modified
    are required
    '''
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def update_accessed(self):
        self.accessed = datetime.now()

    def update_modified(self):
        self.modified = datetime.now()


class Disk:
    '''
    '''
    size = Column(Integer)
    file_count = Column(Integer)


def create_all():
    '''
    Create all tables if they do not already exist in the database.

    Note:
        When this function is called only class objects loaded in the current
        namespace will attempt to be created.
    '''
    Base.metadata.create_all(engine)


@event.listens_for(mapper, 'init')             # Any time an object is created,
def add_to_db(obj, args, kwargs):              # add it to the database session
    '''
    All relational objects are automatically added to the database session on
    instantiation.
    '''
    db_sess.add(obj)


@event.listens_for(Query, 'before_compile')    # Always commit before querying (SELECT)
def commit(*args, **kwargs):
    '''
    Commit all of the objects currently in the session. Note that objects
    are automatically added to the database session (db_sess) and that committing
    these objects does not normally have to be performed manually.
    '''
    try:
        db_sess.commit()
    except:
        db_sess.rollback()
        raise


@event.listens_for(Base, 'before_insert')            # Before inserting a new object
def base_before_insert(mapper, connection, target):  # update its timestamps.
    '''
    Update timestampes and save :class:`~exa.frames.DataFrame` data to disk
    before inserting to the database.
    '''
    print('before insert')


@event.listens_for(Base, 'before_update')            # Before inserting a new object
def base_before_update(mapper, connection, target):  # update its timestamps.
    '''
    Update timestampes and save :class:`~exa.frames.DataFrame` data to disk
    before updating the database.
    '''
    print('before update')


engine_name = Config.relational_engine()
engine = create_engine(engine_name)
DBSession = sessionmaker(bind=engine)
db_sess = DBSession()    # Database session (note that this is an unscoped session)
