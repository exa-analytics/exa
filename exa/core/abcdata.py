# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Abstract Data Objects
#########################
At a minimum

Data consists of dimensions and features. Dimensions describe the extent of the
space occupied by the data. Features describe the individual values at given
points in the space of the data. Dimensions can be defined as discrete arrays
or by parameterized functions. A common example is weather data. The dimensions
of weather are longitude, latitude, and time. The features of weather are
temperature and precipitation.

The number of dimensions determine the dimensionality of the data (in the weather
example there are three dimensions, two spatial and one temporal). There can be
an arbitrary number of features. In computational work it can be useful to perform
'record keeping' which is accomplished by maintaining a unique indentifier (index)
with every point in the space of the data.
"""
from exa.typed import Meta


class ABCDataMeta(Meta):
    """An abstract base metaclass for all data objects."""
    dataid = UUID


class ABCDataBase(six.with_metaclass(ABCDataMeta)):
    """An abstract base class for all data objects."""
    @abstractproperty
    def features(self):
        """List of feature names."""
        pass

    @abstractproperty
    def dimensions(self):
        """List of dimension names."""
        pass

    @abstractproperty
    def uid(self):
        """
        Unique identifier name (for data entries).

        Note:
            The :attr:`~exa.core.abcdata.ABCDataMeta.dataid` is the unique
            identifier of the data object itself (for use by a
            :class:`~exa.core.container.Container`).
        """
        pass
