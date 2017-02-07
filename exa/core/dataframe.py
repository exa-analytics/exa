# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exa DataFrame
###################################
The :class:`~exa.core.dataframe.DataFrame` object supports index aliases and
units.

See Also:
    http://pandas.pydata.org/
"""
import six
import pandas as pd
from exa.core.base import Base
#from exa.core.indexing import indexers


class DataFrame(six.with_metaclass(Base, pd.DataFrame)):
    pass


#for name, indexer in indexers():          # Calls pandas machinery
#    setattr(DataFrame, name, None)           # Need to unreference existing indexer
#    DataFrame._create_indexer(name, indexer) # Prior to instantiation new indexer
import pandas as pd
from exa.core.base import DataObject
#from exa.core.indexing import indexers


class DataFrame(DataObject, pd.DataFrame):    # Note the ordering
    """
    A dataframe is a multiply valued n dimensional array.

    Multiply valued means that at each discrete point in the space covered
    by the (n-dimensional) array, there are a collection of attributes.
    Attributes are given as columns. Each individual colunn is therefore a
    :class:`~exa.core.dataseries.DataSeries` object with the same dimensions
    as that of the dataframe
    """
    _getters = ("compute", )
    _metadata = ['name']

    @property
    def _constructor(self):
        return DataFrame

    def __init__(self, *args, **kwargs):
        units = kwargs.pop("units", None)
        super(DataFrame, self).__init__(*args, **kwargs)


DataFrame._init()
