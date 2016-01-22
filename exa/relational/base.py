# -*- coding: utf-8 -*-
'''
Base Relational Objects
===============================================
'''
from datetime import datetime
from traitlets import MetaHasTraits
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import sessionmaker
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
    def __len__(self):
        commit()
        return session.query(self).count()

    def __iter__(self):
        commit()
        for item in session.query(self).all():
            yield item

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
                return obj_list[0]
        else:
            return obj_list


@as_declarative(metaclass=Meta)
class Base:
    '''
    Declarative base class (used by SQLAlchemy) to initialize relational tables.
    '''
    pkid = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):    # "declared_attr" makes this behave like a property
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

    @classmethod
    def _df(cls):
        '''
        Display a :py:class:`~pandas.DataFrame` representation of the table.
        '''
        commit()
        df = pd.read_sql(session.query(cls).statement, engine.connect())
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
            obj = session.query(cls).filter(cls.pkid == key).all()
            if len(obj) == 1:
                return obj[0]
            else:
                raise PrimaryKeyError(key, cls.__tablename__)
        elif isinstance(key, str):        # Try by name
            if hasattr(cls, 'name'):
                obj = session.query(cls).filter(cls.name == key).all()
                if len(obj) == 1:
                    return obj[0]
                else:
                    raise MultipleObjectsError(key, cls.__tablename__)
            else:
                raise NameKeyError(cls.__tablename__)
        else:
            if hasattr(cls, '_getitem_'):
                return cls._getitem(key)
            raise TypeError('Unsupported key type for {0}'.format(type(key)))

    def __getitem__(self, key):
        commit()
        return self._getitem(key)

    def __repr__(cls):
        return '{0}({1})'.format(cls.__class__.__name__, cls.pkid)


def commit():
    '''
    Commit all of the objects currently in the session. Note that objects
    are automatically added to the database session and that committing
    these objects does not normally have to be performed manually.
    '''
    try:
        session.commit()
    except:
        session.rollback()
        raise               # Catch and raise any and all exceptions


def create_all():
    '''
    '''
    session.flush()
    DeclarativeBase.metadata.create_all(engine)


engine_name = Config.relational_engine()
engine = create_engine(engine_name)
DBSession = sessionmaker(bind=engine)
#TODO: SEE ISSUE #41  session = Session() vs session = scoped_session(sessionmaker(bind=engine))
# For now, non-scoped
dbsession = DBSession()
