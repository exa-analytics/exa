# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Physical Constants
#######################
Table of reference physical constants in SI units.
"""
from sqlalchemy import String, Float, Column
from exa.relational.base import Base, BaseMeta, scoped_session


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


class Constant(Base, metaclass=Meta):
    """
    Physical constants and their values in SI units.

    >>> hartree = Constant['Eh']
    >>> hartree
    4.35974434e-18

    Note:
        Available constants can be inspected by calling:

        .. code-block:: Python

            Constant.to_frame()
    """
    symbol = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    aliases = {'hartree': 'Eh',    # Note that all aliases should be lowercase (see above)
               'faraday': 'F'}

    def __repr__(self):
        return 'Constant({0}: {1})'.format(self.symbol, self.value)
