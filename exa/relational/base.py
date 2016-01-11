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


class Meta(DeclarativeMeta):
    '''
    Extends the default sqlalchemy table metaclass to allow for getting.
    '''

    def df(self):
        '''
        Display a :py:class:`~pandas.DataFrame` representation of the table.
        '''
        commit()
        df = pd.read_sql(
            'SELECT * FROM {0}'.format(self.__tablename__.upper()),
            engine.connect()
        )
        if 'pkid' in df.columns:
            return df.set_index('pkid')
        else:
            return df

    def count(self):
        return session.query(self).count()

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


def cleanup_anon_sessions():
    '''
    Keep only the n most recently accessed anonymous sessions.
    '''
    anons = session.query(Session).filter(
        Session.name == 'anonymous'
    ).order_by(Session.accessed).all()[:-5]
    for anon in anons:
        session.delete(anon)


engine_name = Config.relational_engine()
engine = create_engine(engine_name)
session = scoped_session(sessionmaker(bind=engine))
