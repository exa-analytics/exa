# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Physical Constants
#######################
Table of reference physical constants in SI units.
"""
import six
from sqlalchemy import String, Float, Column
from exa.cms.base import Base, BaseMeta, scoped_session


class Meta(BaseMeta):
    """
    Metaclass for :class:`~exa.relational.constant.Constant`.
    """
    def get_by_symbol(cls, symbol):
        """Get the value of a constant with the given symbol."""
        if symbol.lower() in cls.aliases:
            symbol = cls.aliases[symbol.lower()]
        with scoped_session() as session:
            return session.query(cls).filter(cls.symbol == symbol).one().value

    def _getitem(cls, symbol):
        return cls.get_by_symbol(symbol)


class Constant(six.with_metaclass(Meta, Base)):
    """
    Physical constants and their values in SI units.

        >>> Constant['Eh']
        4.35974434e-18
        >>> Constant['G']
        6.67384e-11

    To see available values:

    .. code-block:: Python

        Constant.to_frame()
    """
    symbol = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    aliases = {'hartree': 'Eh',    # Note that all aliases should be lowercase (see above)
               'faraday': 'F',
               "avogadro's number": 'NA',
               "avogadro number": 'NA'}

    def __repr__(self):
        return 'Constant({0}: {1})'.format(self.symbol, self.value)
