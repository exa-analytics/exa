# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Database access object
####################################
An interface that allows for composing sql queries
with or without a sqlalchemy ORM.
"""
import operator

from traitlets import Dict, List, Unicode, Any
from traitlets import default, validate, TraitError
import numpy as np
import pandas as pd

from exa.core.data import Data


_CHUNKSIZE = 50000

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
    filters = Dict(help='filters to apply')

    @default('entities')
    def _default_entities(self):
        return self.columns

    @validate('schema', 'table_name')
    def _validate_sql(self, prop):
        sql = prop['value']
        if any((i in sql for i in (';', '--'))):
            raise SQLInjectionError("; or -- found. abort")
        return sql

    def _scan_sql(self, query):
        self.log.debug("validating query against sql injection")
        if any((i in query for i in (';', '--'))):
            raise SQLInjectionError("; or -- found. abort")

    def _filter_builder(self, query):
        filters = []
        for column, conditions in self.filters.items():
            for op, cond in conditions:
                fil = "{} {} '{}'".format(column, _raw_op_map[op], cond)
                self.log.debug("building filter {}".format(fil))
                filters.append(fil)
        filters = ' and '.join(filters)
        if filters:
            query += ' where {}'.format(filters)
        return query

    def _query_builder(self, query):
        entities = ', '.join(self.entities) or '*'
        query = 'select {} from {}'.format(entities, self.fqtn())
        query = self._filter_builder(query)
        self._scan_sql(query)
        return query + ';'

    def _upload(self, session, payload):
        if self.schema:
            try:
                session.execute(
                    'create schema if not exists {};'.format(self.schema)
                )
                session.commit()
            except Exception as e:
                self.log.error("could not create schema: {}".format(e))
        # TODO : implement and validate uniqueness constraints
        #        on the Data class before insertion
        payload.to_sql(
            self.table_name, session.bind, index=False,
            schema=self.schema, if_exists='append',
        )

    def __call__(self, session, payload=None, query_only=False):
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
        return '{self.schema}.{self.table_name}'.format(self=self)


class DAO(RawDAO):
    """
    When provided a sqlalchemy declarative
    class that contains Table definitions, the DAO can
    provide richer functionality by use of the `related`
    trait.  It is similar in spirit to the `filters` dictionary
    but its outer keys are table names themselves, whose
    values mimic the schema of filters itself. There is
    additionally a reserved key, 'links', which is where
    the table relationships are defined.

    .. code-block:: Python

        dao = exa.core.dao.DAO(table_name='users')
        dao.filters = {
            'id': [('gt', 1), ('lt', 10)],
            'user': [('eq', 'foo')]
        }
        # specify any number of related fields and links
        dao.related = {
            'orders': {
                'entities': ['total_cost', 'date'],
                'filters': {
                    'order_date': [('ge', '2020-01-01')]
                }
            },
            'links': {
                'users.id': [('eq', 'orders.user_id')]
            }
        }
        dao(session=sqlalchemy.Session())
    """
    table_obj = Any(help='a sqlalchemy table')
    related = Dict(help='relationships between tables')
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
                "no table {} in base.metadata.tables".format(fqtn)
            )
        for table in self.related:
            if table == 'links': continue
            if table not in base.metadata.tables.keys():
                raise TraitError(
                    "no table {} in base.metadata.tables".format(table)
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

    def _upload(self, session, payload, chunksize=_CHUNKSIZE):
        """Use sqlalchemy's bulk insert to upload the
        payload data in chunks after it has been validated.

        Args:
            session (session): a DB session (see :mod:`~sqlalchemy.orm.sessionmaker`)
            payload (pd.DataFrame): data to upload
            chunksize (int): number of records to load at a time
        """
        payload = self._validate_data(payload, reverse=True)
        table = self.table_obj
        for _, group in payload.groupby(
                np.arange(len(payload.index)) // chunksize):
            start = self.right_now()
            session.execute(
                table.insert(), group.to_dict(orient='records')
            )
            self.log.info("{} loaded {} records in {}".format(
                self.fqtn(), len(group.index), self.time_diff(start)
            ))

    def _query_builder(self, query):
        entities = self._entities_builder()
        if entities:
            query = query.with_entities(*entities)
        query = self._filter_builder(query)
        query = self._related_builder(query)
        return query

    def _entities_builder(self):
        entities = [self.table_obj.columns[col] for col in self.entities]
        for table, params in self.related.items():
            if table == 'links': continue
            table = self.base.metadata.tables[table]
            entities.extend([
                table.columns[column] for column in params.get('entities', [])
            ])
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

    def _related_builder(self, query):
        for left, links in self.related.get('links', {}).items():
            *left_table, left_column = left.split('.')
            for operator, right in links:
                *right_table, right_column = right.split('.')
                t1 = self.base.metadata.tables['.'.join(left_table)]
                t2 = self.base.metadata.tables['.'.join(right_table)]
                op = _op_map.get(operator, None)
                if op is None:
                    self.log.warning(f"{operator} not understood. skipping")
                    continue
                query = query.filter(op(t1.columns[left_column], t2.columns[right_column]))
        return query
