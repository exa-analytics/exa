# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0

import sys

import pytest
import pandas as pd
from traitlets import TraitError

try:
    import sqlalchemy as sq
    from sqlalchemy import Column, Integer, String, Table
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    import psycopg2
except ImportError:
    pass

import exa
from exa.core.dao import DAO, RawDAO, SQLInjectionError

sqla = pytest.mark.skipif(
    'sqlalchemy' not in sys.modules, reason='requires sqlalchemy'
)
psyc = pytest.mark.skipif(
    'psycopg2' not in sys.modules, reason='requires psycopg2'
)
pg_db_conn = pytest.mark.skipif(
    not (exa.cfg.db_conn.startswith('postgres') or
         exa.cfg.db_conn.startswith('psycopg')),
    reason='requires DB connection string'
)
SCHEMA1 = 'exa_test_schema'
SCHEMA2 = 'exa_test_other'

def new_session(eng):
    Session = sessionmaker()
    Session.configure(bind=eng)
    session = Session()
    return session

@sqla
@pytest.fixture(scope='module')
def empty_sqlite_session():
    eng = sq.create_engine('sqlite:///')
    Session = sessionmaker()
    Session.configure(bind=eng)
    session = Session()
    yield session
    session.close()

@psyc
@pg_db_conn
@pytest.fixture(scope='module')
def empty_postgres_session():
    eng = sq.create_engine(exa.cfg.db_conn)
    Session = sessionmaker()
    Session.configure(bind=eng)
    session = Session()
    yield session
    session.close()

@sqla
@pytest.fixture(scope='module')
def test_base():
    Base = declarative_base()

    class Foo(Base):
        __tablename__ = 'foo'
        __table__ = Table(
            'foo', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String))

    class Bar(Base):
        __tablename__ = 'bar'
        __table__ = Table(
            'bar', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            schema=SCHEMA1)

    class Quu(Base):
        __tablename__ = 'quu'
        __table__ = Table(
            'quu', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('foo_name', String),
            Column('bar_name', String),
            schema=SCHEMA2)

    class Qux(Base):
        __tablename__ = 'qux'
        __table__ = Table(
            'qux', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('bar_name', String))

    f = Foo()
    b = Bar()
    q = Quu()
    x = Qux()
    assert isinstance(f, Base)
    assert isinstance(b, Base)
    assert isinstance(q, Base)
    assert isinstance(x, Base)
    return Base

@psyc
@pg_db_conn
@pytest.fixture(scope='module')
def postgres_engine_wipe_base(test_base):
    d = psycopg2.Date
    assert d is not None
    eng = sq.create_engine(exa.cfg.db_conn)
    wipe = "truncate {};".format
    eng.execute("create schema if not exists {};".format(SCHEMA1))
    eng.execute("create schema if not exists {};".format(SCHEMA2))
    test_base.metadata.create_all(bind=eng)
    yield eng, wipe, test_base
    eng.execute("drop schema if exists {} cascade;".format(SCHEMA1))
    eng.execute("drop schema if exists {} cascade;".format(SCHEMA2))

@sqla
@pytest.fixture(scope='module')
def sqlite_engine_wipe_base(test_base):
    eng = sq.create_engine('sqlite:///')
    wipe = "delete from {};".format
    eng.execute("attach ':memory:' as {};".format(SCHEMA1))
    eng.execute("attach ':memory:' as {};".format(SCHEMA2))
    test_base.metadata.create_all(bind=eng)
    yield eng, wipe, test_base

@pytest.fixture(scope='module')
def base_data():
    return {
        'bar': pd.DataFrame.from_dict({
            'id': [1, 2, 3],
            'name': ['a', 'b', 'c']
        }),
        'foo': pd.DataFrame.from_dict({
            'id': [1, 2, 3],
            'name': ['a', 'b', 'c']
        }),
        'quu': pd.DataFrame.from_dict({
            'id': [1, 2, 3],
            'foo_name': ['b', 'd', 'f'],
            'bar_name': ['a', 'c', 'g']
        }),
        'qux': pd.DataFrame.from_dict({
            'id': [5, 6, 7],
            'bar_name': ['c', 'g', 'e']
        })
    }

@sqla
def test_raw_dao_sqlite(empty_sqlite_session):
    dao = RawDAO(table_name='sqlite_master')
    df = dao(session=empty_sqlite_session)
    assert isinstance(df, pd.DataFrame)
    q = dao(session=empty_sqlite_session, query_only=True)
    assert isinstance(q, str)

@psyc
@pg_db_conn
def test_raw_dao_postgres(empty_postgres_session):
    dao = RawDAO(schema='information_schema', table_name='columns')
    df = dao(session=empty_postgres_session)
    assert isinstance(df, pd.DataFrame)
    q = dao(session=empty_postgres_session, query_only=True)
    assert isinstance(q, str)

@sqla
def test_raw_dao_no_sql_injection_sqlite(empty_sqlite_session):
    dao = RawDAO(table_name='sqlite_master')
    dao.entities = ['; drop table students;']
    with pytest.raises(SQLInjectionError):
        dao(session=empty_sqlite_session)

@psyc
@pg_db_conn
def test_raw_dao_no_sql_injection_postgres(empty_postgres_session):
    dao = RawDAO(schema='information_schema', table_name='columns')
    dao.entities = ['; drop table students;']
    with pytest.raises(SQLInjectionError):
        dao(session=empty_postgres_session)

@sqla
def test_raw_dao_filter_builder_sqlite(sqlite_engine_wipe_base):
    eng, wipe, _ = sqlite_engine_wipe_base
    session = new_session(eng)
    dao = RawDAO(table_name='foo')
    session.execute(
        "create table if not exists foo ( "
        "id integer serial, name text );"
    )
    session.execute(
        "insert into foo (id, name) "
        "values (1, 'a'), (2, 'b'), (3, 'c');"
    )
    dao.filters = {'id': [('gt', 1)], 'name': [('eq', 'c')]}
    df = dao(session=session)
    assert df.shape == (1, 2)
    session.execute(wipe('foo'))
    session.commit()
    session.close()

@psyc
@pg_db_conn
def test_raw_dao_filter_builder_postgres(postgres_engine_wipe_base):
    eng, wipe, _ = postgres_engine_wipe_base
    session = new_session(eng)
    dao = RawDAO(table_name='foo')
    session.execute(
        "create table if not exists foo ( "
        "id integer primary key, name text );"
    )
    session.execute(
        "insert into foo (id, name) "
        "values (1, 'a'), (2, 'b'), (3, 'c');"
    )
    session.commit()
    dao.filters = {'id': [('gt', 1)], 'name': [('eq', 'c')]}
    df = dao(session=session)
    assert df.shape == (1, 2)
    session.execute(wipe('foo'))
    session.commit()
    session.close()

def round_trip_bar(engine_wipe_base, data):
    eng, wipe, base = engine_wipe_base
    session = new_session(eng)
    bar = DAO(schema=SCHEMA1, table_name='bar', base=base)
    bar(session=session, payload=data)
    session.commit()
    df = bar(session=session)
    assert df.shape == (3, 2)
    session.execute(wipe('{}.bar'.format(SCHEMA1)))
    session.commit()
    df = bar(session=session)
    assert df.empty
    session.close()

@sqla
def test_round_trip_bar_sqlite(sqlite_engine_wipe_base, base_data):
    round_trip_bar(sqlite_engine_wipe_base, base_data['bar'])

@psyc
@pg_db_conn
def test_round_trip_bar_postgres(postgres_engine_wipe_base, base_data):
    round_trip_bar(postgres_engine_wipe_base, base_data['bar'])

def dao_filter_builder_foo(engine_wipe_base, data):
    eng, wipe, base = engine_wipe_base
    session = new_session(eng)
    dao = DAO(
        table_name='foo', base=base,
        filters={'id': [('gt', 1)], 'name': [('eq', 'c')]}
    )
    dao(session=session, payload=data)
    session.commit()
    df = dao(session=session)
    assert df.shape == (1, 2)
    session.execute(wipe('foo'))
    session.commit()
    session.close()

@sqla
def test_dao_filter_builder_foo_sqlite(sqlite_engine_wipe_base, base_data):
    dao_filter_builder_foo(sqlite_engine_wipe_base, base_data['foo'])

@psyc
@pg_db_conn
def test_dao_filter_builder_foo_postgres(postgres_engine_wipe_base, base_data):
    dao_filter_builder_foo(postgres_engine_wipe_base, base_data['foo'])

@sqla
def test_dao_entities_builder_sqlite(sqlite_engine_wipe_base, base_data):
    eng, wipe, base = sqlite_engine_wipe_base
    session = new_session(eng)
    bar = DAO(schema=SCHEMA1, entities=['id'], table_name='bar', base=base)
    bar(session=session, payload=base_data['bar'])
    df = bar(session=session)
    assert df.shape == (3, 1)
    session.execute(wipe('{}.bar'.format(SCHEMA1)))
    session.close()

@sqla
def test_dao_entities_sqlite(sqlite_engine_wipe_base, base_data):
    eng, wipe, base = sqlite_engine_wipe_base
    session = new_session(eng)
    session.execute(wipe('foo'))
    foo = DAO(table_name='foo', base=base)
    foo(session=session, payload=base_data['foo'])
    session.commit()
    foo.entities = ['id']
    foo.filters = {'id': [('dne', 0)]}
    df = foo(session=session)
    assert df.shape == (3, 1)

    quu = DAO(schema=SCHEMA2, table_name='quu', base=base)
    quu(session=session, payload=base_data['quu'])
    session.commit()
    quu.entities = ['id', 'foo_name']
    df = quu(session=session)
    assert df.shape == (3, 2)

    foo.related = {
        '{}.quu'.format(SCHEMA2): {
            'entities': ['bar_name'],
            'filters': {},
        },
        'links': {
            'foo.name': [('eq', '{}.quu.bar_name'.format(SCHEMA2)),
                         ('dne', '{}.quu.foo_name'.format(SCHEMA2))]
        }
    }

    df = foo(session=session)
    assert df.shape == (2, 2)
    q = foo(session=session, query_only=True)
    assert isinstance(q, sq.orm.Query)
    session.execute(wipe('foo'))
    session.execute(wipe('exa_test_other.quu'))
    session.commit()
    session.close()

@sqla
def test_fqtn(sqlite_engine_wipe_base):
    *_, base = sqlite_engine_wipe_base
    qux = DAO(table_name='qux', base=base)
    foo = DAO(table_name='foo', base=base)
    bar = DAO(schema=SCHEMA1, table_name='bar', base=base)
    quu = DAO(schema=SCHEMA2, table_name='quu', base=base)
    assert qux.fqtn() == 'qux'
    assert foo.fqtn() == 'foo'
    assert quu.fqtn() == 'exa_test_other.quu'
    assert bar.fqtn() == 'exa_test_schema.bar'

@sqla
def test_dao_invalid_table_sqlite(sqlite_engine_wipe_base):
    *_, base = sqlite_engine_wipe_base
    with pytest.raises(TraitError):
        DAO(table_name='dne', base=base)
    with pytest.raises(TraitError):
        DAO(table_name='foo', base=base,
            related={'dne': {'entities': [], 'filters': []}})
