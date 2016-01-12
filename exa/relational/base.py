# -*- coding: utf-8 -*-
'''
Base Relational Objects
===============================================
'''
from sqlalchemy import Column, Integer, DateTime, Float, String
from sqlalchemy import ForeignKey, Table
from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, mapper, relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from datetime import datetime
from exa import Config
from exa import _pd as pd
from exa.relational.errors import PrimaryKeyError, NameKeyError, MultipleObjectsError


class Meta(DeclarativeMeta):
    '''
    '''
    def __len__(self):
        commit()
        return session.query(self).count()

    def __iter__(self):
        commit()
        for item in session.query(self).all():
            yield item

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
        sql = 'SELECT * FROM {0}'
        tbl = cls.__tablename__.upper()
        commit()
        df = pd.read_sql(sql.format(tbl), engine.connect())
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


engine_name = Config.relational_engine()
engine = create_engine(engine_name)
session = scoped_session(sessionmaker(bind=engine))
