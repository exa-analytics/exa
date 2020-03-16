# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Database access object
####################################
An interface that allows for composing sql queries
with or without a sqlalchemy ORM.
"""
import operator

from traitlets import Dict, List, Unicode, Any, Integer
from traitlets import default, validate, TraitError
import numpy as np
import pandas as pd

from exa.core.data import Data


_op_map = {
    k.rstrip('_'): getattr(operator, k) for k in [
        'lt', 'le', 'eq',
        'ne', 'ge', 'gt',
        'not_', 'and_', 'or_'
    ]
}

_raw_op_map = {
    'lt': '<', 'le': '<=', 'eq': '=',
    'ne': '!=', 'ge': '>=', 'gt': '>',
    'not': 'not', 'and': 'and', 'or': 'or'
}

class SQLInjectionError(Exception):
    pass


class RawDAO(Data):
    """The so-called database access object (DAO).

    The DAO models a single table in a database.
    Specify a schema and table_name to obtain raw
    DAO functionality, a quick and dirty query
    builder for low-overhead pythonic database access.

    Control the columns being pulled with `entities`
    and the amount of data to be pulled with `filters`.
    filters is a well-formed dictionary with an
    expected schema:

    .. code-block:: Python

        dao = exa.core.dao.RawDAO(table_name='users')
        # if not specified, fetches all columns
        dao.entities = ['id', 'user']
        # if not specified, fetches all rows
        dao.filters = {
            'id': [('gt', 1), ('lt', 10)],
            'user': [('eq', 'foo')]
        }
        df = dao(session=sqlalchemy.Session())

    """
    schema = Unicode(help='schema name')
    table_name = Unicode(help='table name')
    entities = List(help='columns to pull')
    groupbys = List(help='columns to group by') # TODO
    orderbys = List(help='columns to sort by') # TODO
    order_dir = Unicode(help='sort direction') # TODO
    functions = Dict(help='functions to apply per column') # TODO
    filters = Dict(help='filters to apply per column')
    havings = Dict(help='having conditions') # TODO
    chunksize = Integer(50000, help='number of records to load at a time')
    __invalid_tokens = [';', '--', '/*']

    @default('entities')
    def _default_entities(self):
        return self.columns

    @validate('schema', 'table_name', 'entities',
              'groupbys', 'orderbys', 'order_dir')
    def _validate_sql(self, prop):
        self._scan_sql(prop['value'])
        return prop['value']

    def _scan_sql(self, query):
        self.log.debug(f'validating "{query}" against sql injection')
        for token in self.__invalid_tokens:
            if token in query:
                raise SQLInjectionError("invalid token found. abort")

    def _filter_builder(self, query):
        filters = []
        for column, conditions in self.filters.items():
            for op, cond in conditions:
                sql_op = _raw_op_map.get(op, None)
                if sql_op is None:
                    self.log.warning(f"{op} not understood. skipping")
                    continue
                fil = f"{column} {sql_op} '{cond}'"
                self.log.debug(f"building filter {fil}")
                filters.append(fil)
        filters = ' and '.join(filters)
        if filters:
            query += f' where {filters}'
        return query

    def _query_builder(self, query):
        entities = ', '.join(self.entities) or '*'
        query = f'select {entities} from {self.fqtn()}'
        query = self._filter_builder(query)
        self._scan_sql(query)
        return query + ';'

    def _upload(self, session, payload):
        """Use pd.DataFrame.to_sql to upload the
        payload data in chunks after it has been validated.

        Args:
            session (session): a DB session (see :mod:`~sqlalchemy.orm.sessionmaker`)
            payload (pd.DataFrame): data to upload
        """
        payload = self._validate_data(payload, reverse=True)
        fqtn = self.fqtn()
        nrec = len(payload.index)
        if nrec > self.chunksize:
            chunks = -(-nrec // self.chunksize)
            self.log.warning(f"{fqtn} loading {nrec} records in {chunks} chunks")
        bt = self.right_now()
        payload.to_sql(
            self.table_name, session.bind, index=False,
            schema=self.schema, if_exists='append',
            chunksize=self.chunksize,
        )
        self.log.info(f"{fqtn} loading {nrec} records took {self.time_diff(bt)}")

    def __call__(self, session, payload=None, query_only=False):
        """Primary public API for the RawDAO. Default
        behavior is to fetch data. If provided a payload,
        will attempt to upload that data after validation.

        Args:
            session (session): a DB session (see :mod:`~sqlalchemy.orm.sessionmaker`)
            payload (pd.DataFrame): data to upload (optional)
            query_only (bool): if True, return the query unevaluated
        """
        if payload is not None:
            return self._upload(session, payload)
        query = self._query_builder('')
        if query_only:
            return query
        self._data = pd.read_sql(query, session.bind)
        return self._data

    def fqtn(self):
        if not self.schema:
            return self.table_name
        return f'{self.schema}.{self.table_name}'

    def create_schema(self, session):
        if self.schema:
            try:
                session.execute(
                    f'create schema if not exists {self.schema};'
                )
                session.commit()
            except Exception as e:
                self.log.error(f"could not create schema: {e}")

class DAO(RawDAO):
    """
    When provided a sqlalchemy declarative
    class that contains Table definitions, the DAO can
    provide richer query and validation functionality.

    .. code-block:: Python

        base = sqlalchemy.ext.declarative.declarative_base()
        table = sqlalchemy.Table(..., base.metadata, ...)
        dao = exa.core.dao.DAO(table_name='users', base=base)
        dao.filters = {
            'id': [('gt', 1), ('lt', 10)],
            'user': [('eq', 'foo')]
        }
        dao(session=sqlalchemy.Session())
    """
    table_obj = Any(help='a sqlalchemy table')
    base = Any(help='a sqlalchemy declarative base class')

    @validate('base')
    def _validate_base(self, prop):
        """Validate that all tables mentioned in
        the DAO attributes exist in the base table
        class metadata."""
        base = prop['value']
        fqtn = self.fqtn()
        if fqtn not in base.metadata.tables.keys():
            raise TraitError(
                f"no table {fqtn} in base.metadata.tables"
            )
        return base

    @default('table_obj')
    def _default_table_obj(self):
        return self.base.metadata.tables[self.fqtn()]

    def __call__(self, session, payload=None, query_only=False):
        """Primary public API for the DAO. Default
        behavior is to fetch data. If provided a payload,
        will attempt to upload that data after validation.

        Args:
            session (session): a DB session (see :mod:`~sqlalchemy.orm.sessionmaker`)
            payload (pd.DataFrame): data to upload (optional)
            query_only (bool): if True, return the query unevaluated
        """
        if payload is not None:
            return self._upload(session, payload)
        self._validate_base({'value': self.base})
        query = self._query_builder(session.query(self.table_obj))
        if query_only:
            return query
        self._data = pd.read_sql(query.statement, session.bind)
        return self._data

    def _upload(self, session, payload):
        """Use sqlalchemy's bulk insert to upload the
        payload data in chunks after it has been validated.

        Args:
            session (session): a DB session (see :mod:`~sqlalchemy.orm.sessionmaker`)
            payload (pd.DataFrame): data to upload
        """
        payload = self._validate_data(payload, reverse=True)
        fqtn = self.fqtn()
        table = self.table_obj
        for _, group in payload.groupby(
                np.arange(len(payload.index)) // self.chunksize):
            start = self.right_now()
            session.execute(
                table.insert(), group.to_dict(orient='records')
            )
            dt = self.time_diff(start)
            self.log.info(f"{fqtn} loaded {len(group.index)} records in {dt}")

    def _query_builder(self, query):
        entities = self._entities_builder()
        if entities:
            query = query.with_entities(*entities)
        query = self._filter_builder(query)
        return query

    def _entities_builder(self):
        entities = [self.table_obj.columns[col] for col in self.entities]
        return entities

    def _filter_builder(self, query):
        for column, conditions in self.filters.items():
            if isinstance(column, str):
                column = self.table_obj.columns[column]
            for operator, condition in conditions:
                query = self._filter_applier(query, column, operator, condition)
        return query

    def _filter_applier(self, query, column, operator, condition):
        op = _op_map.get(operator, None)
        if op is None:
            self.log.warning(f"{operator} not understood. skipping")
            return query
        return query.filter(op(column, condition))
