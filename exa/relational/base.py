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
from datetime import datetime
from traitlets import MetaHasTraits
from sqlalchemy import Column, Integer, create_engine, event
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from exa import Config
from exa import _pd as pd
from exa.relational.errors import PrimaryKeyError, NameKeyError, MultipleObjectsError, NoObjectsError


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
    def table_dataframe(cls):
        '''
        Display a :py:class:`~pandas.DataFrame` representation of the table.
        '''
        df = pd.read_sql(db_sess.query(cls).statement, engine.connect())
        if 'pkid' in df.columns:
            return df.set_index('pkid')
        else:
            return df

    @classmethod
    def load(cls, key):
        '''
        Load an object entry from the database.
        '''
        commit()
        if isinstance(key, int):          # Assume primary key
            obj = db_sess.query(cls).filter(cls.pkid == key).all()
            return cls._return(obj, key)
        elif isinstance(key, str):        # Try by name
            if hasattr(cls, 'name'):
                obj = db_sess.query(cls).filter(cls.name == key).all()
                return cls._return(obj, key)
            else:
                raise NameKeyError(cls.__tablename__)
        else:
            raise TypeError('Unsupported key type for {0}'.format(type(key)))

    def _return(self, obj_list, key, single=True):
        '''
        Checks the count of the to-be-returned object list to make sure that it
        matches what is expected.
        '''
        if len(obj_list) == 0:
            raise NoObjectsError(key, self)
        if single:
            if len(obj_list) > 1:
                raise MultipleObjectsError(key, self)
            else:
                obj = obj_list[0]
                obj.__accessed__ = True
                return obj
        else:
            for obj in obj_list:
                obj.__accessed__ = True
            return obj_list

    def __getitem__(self, key):
        '''
        By default, slicing on relational tables simply loads the entry or entries sliced
        from the table.
        '''
        commit()
        return self.load(key)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__modified__ = True
        self.__accessed__ = True

    def __repr__(cls):
        return '{0}({1})'.format(cls.__class__.__name__, cls.pkid)


@event.listens_for(Query, 'before_compile')    # Always commit before querying (SELECT)
def commit(*args, **kwargs):
    '''
    Commit all of the objects currently in the session. Note that objects
    are automatically added to the database session and that committing
    these objects does not normally have to be performed manually.
    '''
    try:
        db_sess.commit()
    except:
        db_sess.rollback()
        raise               # Catch and raise any and all exceptions


def create_all():
    '''
    '''
    Base.metadata.create_all(engine)


engine_name = Config.relational_engine()
engine = create_engine(engine_name)
DBSession = sessionmaker(bind=engine)
#TODO: SEE ISSUE #41  session = Session() vs session = scoped_session(sessionmaker(bind=engine))
# For now, non-scoped
db_sess = DBSession()
