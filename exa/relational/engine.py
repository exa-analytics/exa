# -*- coding: utf-8 -*-
'''
Database Installation
#########################################

'''
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from exa._config import config
from exa.relational.base import Base
from exa.relational.unit import (Length, Mass, Time, Current, Amount, Luminosity,
                                 Dose, Acceleration, Charge, Dipole, Energy,
                                 Force, Frequency, MolarMass)
from exa.relational.isotope import Isotope
from exa.relational.constant import Constant
from exa.relational.file import File
from exa.relational.container import Container


engine = None
SessionFactory = None


def to_frame(klass):
    '''
    '''
    with scoped_session() as s:
        df = pd.read_sql(s.query(cls).statement, engine)
    if 'pkid' in df:
        df = df.set_index('pkid').sort_index()
    return df


def create_tables():
    '''
    '''
    Base.metadata.create_all(engine)


def install():
    '''
    '''
    global engine
    global SessionFactory
    engine = create_engine(config['exa_relational'])
    SessionFactory = sessionmaker(bind=engine)


def cleanup():
    '''
    '''
    engine.dispose()


@contextmanager
def scoped_session(*args, **kwargs):
    '''
    '''
    session = SessionFactory(*args, **kwargs)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
