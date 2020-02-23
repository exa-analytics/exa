# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0

import os
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
from exa.core.dao import DAO, RawDAO

sqla = pytest.mark.skipif(
    'sqlalchemy' not in sys.modules, reason='requires sqlalchemy'
)
psyc = pytest.mark.skipif(
    'psycopg2' not in sys.modules, reason='requires psycopg2'
)
db_conn = pytest.mark.skipif(
    not bool(exa.cfg.db_conn), reason='requires DB connection string'
)

@sqla
@pytest.fixture(scope='module')
def sqlite_session():
    eng = sq.create_engine('sqlite:///')
    Session = sessionmaker()
    Session.configure(bind=eng)
    session = Session()
    yield session
    session.close()

@sqla
@pytest.fixture(scope='module')
def session_wipe_base():
    conn_str = exa.cfg.db_conn
    conn_str = 'sqlite:///'
    eng = sq.create_engine(conn_str)
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
            schema='exa_test_schema')

    class Quu(Base):
        __tablename__ = 'quu'
        __table__ = Table(
            'quu', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('foo_name', String),
            Column('bar_name', String),
            schema='exa_test_other')

    class Qux(Base):
        __tablename__ = 'qux'
        __table__ = Table(
            'qux', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('bar_name', String))

    if 'sqlite' in conn_str:
        wipe = "delete from {};".format
        eng.execute("attach ':memory:' as exa_test_other;")
        eng.execute("attach ':memory:' as exa_test_schema;")
    else:
        wipe = "truncate {};".format
        eng.execute("create schema exa_test_other;")
        eng.execute("create schema exa_test_schema;")

    Base.metadata.create_all(bind=eng)
    Session = sessionmaker()
    Session.configure(bind=eng)
    session = Session()
    yield session, wipe, Base
    session.execute(wipe('foo'))
    session.execute(wipe('qux'))
    session.execute(wipe('exa_test_other.quu'))
    session.execute(wipe('exa_test_schema.bar'))
    if 'sqlite' not in conn_str:
        session.execute("drop schema if exists exa_test_other cascade;")
        session.execute("drop schema if exists exa_test_schema cascade;")
    session.close()

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
def test_raw_dao_sqlite(sqlite_session):
    dao = RawDAO(table_name='sqlite_master')
    df = dao(session=sqlite_session)
    assert isinstance(df, pd.DataFrame)
    q = dao(session=sqlite_session, query_only=True)
    assert isinstance(q, str)

@sqla
def test_raw_dao_no_sql_injection(sqlite_session):
    dao = RawDAO(table_name='sqlite_master')
    dao.entities = ['; drop table students;']
    with pytest.raises(Exception):
        dao(session=sqlite_session)

@sqla
def test_raw_dao_filter_builder(session_wipe_base):
    session, wipe, base = session_wipe_base
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

@sqla
def test_base(session_wipe_base, base_data):
    session, wipe, base = session_wipe_base
    bar = DAO(schema='exa_test_schema', table_name='bar', base=base)
    bar(session=session, payload=base_data['bar'])
    session.commit()
    df = bar(session=session)
    assert df.shape == (3, 2)
    session.execute(wipe('exa_test_schema.bar'))
    session.commit()
    df = bar(session=session)
    assert df.empty

@sqla
def test_dao_filter_builder(session_wipe_base, base_data):
    session, wipe, base = session_wipe_base
    dao = DAO(
        table_name='foo', base=base,
        filters={'id': [('gt', 1)], 'name': [('eq', 'c')]}
    )
    dao(session=session, payload=base_data['foo'])
    df = dao(session=session)
    assert df.shape == (1, 2)
    session.execute(wipe('foo'))
    session.commit()


@sqla
def test_dao_invalid_table(session_wipe_base):
    *_, base = session_wipe_base
    with pytest.raises(TraitError):
        DAO(table_name='dne', base=base)
    with pytest.raises(TraitError):
        DAO(table_name='foo', base=base,
            related={'dne': {'entities': [], 'filters': []}})

@sqla
def test_dao_entities_builder(session_wipe_base, base_data):
    session, wipe, base = session_wipe_base
    bar = DAO(schema='exa_test_schema', table_name='bar', base=base)
    bar(session=session, payload=base_data['bar'])
    session.execute(wipe('exa_test_schema.bar'))


@sqla
def test_dao_entities(session_wipe_base, base_data):
    session, wipe, base = session_wipe_base
    session.execute(wipe('foo'))
    foo = DAO(table_name='foo', base=base)
    foo(session=session, payload=base_data['foo'])
    session.commit()
    foo.entities = ['id']
    df = foo(session=session)
    assert df.shape == (3, 1)

    quu = DAO(schema='exa_test_other', table_name='quu', base=base)
    quu(session=session, payload=base_data['quu'])
    session.commit()
    quu.entities = ['id', 'foo_name']
    df = quu(session=session)
    assert df.shape == (3, 2)

    foo.related = {
        'exa_test_other.quu': {
            'entities': ['bar_name'],
            'filters': {},
        },
        'links': {
            'foo.name': [('eq', 'exa_test_other.quu.bar_name')]
        }
    }

    df = foo(session=session)
    assert df.shape == (2, 2)
    q = foo(session=session, query_only=True)
    assert isinstance(q, sq.orm.Query)
    session.execute(wipe('foo'))
    session.execute(wipe('exa_test_other.quu'))
    session.commit()

@sqla
def test_fqtn(session_wipe_base, base_data):
    session, wipe, base = session_wipe_base
    qux = DAO(table_name='qux', base=base)
    foo = DAO(table_name='foo', base=base)
    quu = DAO(schema='exa_test_other', table_name='quu', base=base)
    bar = DAO(schema='exa_test_schema', table_name='bar', base=base)
    assert qux.fqtn() == 'qux'
    assert foo.fqtn() == 'foo'
    assert quu.fqtn() == 'exa_test_other.quu'
    assert bar.fqtn() == 'exa_test_schema.bar'

@psyc
@db_conn
@pytest.fixture(scope='module')
def postgres_session():
    eng = sq.create_engine(exa.cfg.db_conn)
    Session = sessionmaker()
    Session.configure(bind=eng)
    session = Session()
    yield session
    session.close()

@psyc
@db_conn
def test_raw_dao_postgres(postgres_session):
    dao = RawDAO(
        schema='information_schema',
        table_name='columns'
    )
    df = dao(session=postgres_session)
    assert isinstance(df, pd.DataFrame)
