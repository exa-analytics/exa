# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data Objects
#########################
Data consists of dimensions and features. Dimensions describe the extent of the
space occupied by the data. Features describe the individual values at given
points in the space of the data. Dimensions can be defined as discrete arrays
or by parameterized functions. A common example is weather data. The dimensions
of weather are longitude, latitude, and time. The features of weather are
temperature and precipitation.

The number of dimensions determine the dimensionality of the data (in the weather
example there are three dimensions, two spatial and one temporal). There can be
an arbitrary number of features. In computational work it can be useful to perform
'record keeping' which is accomplished by maintaining a unique index with every
point in the space of the data.

Default data objects are built using `pandas`_ TODO

.. _pandas: http://pandas.pydata.org/
"""
#import six
#import pandas as pd
#from uuid import UUID, uuid4
#from abc import abstractproperty
#from exa.typed import Meta
#
#
#index_types = (pd.core.index.RangeIndex, pd.core.index.Int64Index,
#               pd.core.index.CategoricalIndex)
#
#
#class GenericMeta(Meta):
#    """
#    Metaclass for generic data objects.
#
#    All data objects must have a unique id. This identifier is used by
#    :class:`~exa.core.container.Container` objects to disambiguate different
#    data objects with similar (or same) names, dimensions, and attributes
#    """
#    uid = UUID
#
#
## Default dat objects rely on pandas machinery
#class ABCData(GenericMeta, pd.core.generic.NDFrame):
#    """Abstract base class for default data objects."""
#    _metadata = ["name", "uid", "units"]
#
#    @property
#    def metadata(self):
#        """Return a dictionary of metadata."""
#        return {name: getattr(self, name) for name in self._metadata}
#
#    @property
#    def features(self):
#        """Return a list of feature names."""
#        if self.dims is not None:
#            return [col for col in self.columns if col not in self.dims]
#        return [col for col in self.columns]
#
#    @property
#    def dimensions(self):
#        """Return a list of dimension names."""
#        if self.dims is None:
#            return []
#        return self.dims
#
#    @abstractproperty
#    def _constructor(self):
#        """Used by pandas to finalize object creation."""
#        pass
#
#    @classmethod
#    def _create_indexers(cls, indexers):
#        """Wrapper around :func:`~pandas.core.generic.NDFrame._create_indexer`."""
#        for name, indexer in indexers:
#            setattr(cls, name, None)
#            cls._create_indexer(name, indexer)
#
#
#class DataMeta(six.with_metaclass(enericMeta):
#    """Metaclass for :class:`~exa.core.data.Data`."""
#    _getters = ("compute", )
#    units = dict
#    dims = list
#
#
#class Data(six.with_metaclass(DataMeta, ABCData, pd.DataFrame)):
#    """A multiply featured, n-dimensional data object."""
#    def as_dimensional(self):
#        """Return a multi-indexed object with dimensions as indices."""
#        if self.dims is not None:
#            return self.reset_index().set_index(self.dims)
#
#    def __init__(self, *args, **kwargs):
#        uid = kwargs.pop('uid', uuid4())
#        units = kwargs.pop('units', None)
#        dims = kwargs.pop('dims', None)
#        super(Data, self).__init__(*args, **kwargs)
#        self.uid = uid
#        self.units = units
#        self.dims = dims
#        if not isinstance(self.index, index_types):
#            self.reset_index(inplace=True)
#        self.index.name = "idx"
#
#
#class BaseSectionIndexer(object):
#    def __init__(self, data):
#        self._data = data
#
#    def __getitem__(self, *args, **kwargs):
#        print(args, kwargs)
#
#
#class SectionIndexer(BaseSectionIndexer):
#    pass
#
#
#class ISectionIndexer(BaseSectionIndexer):
#    pass
#
#
#def get_indexers():
#    """Return a list of indexers."""
#    return [("sec", SectionIndexer), ("isec", ISectionIndexer)]
#
#
#ABCData._create_indexers(get_indexers())
