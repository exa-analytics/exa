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
#from exa.core.base import Base
#from exa.core.indexing import indexers


#class DataFrame(six.with_metaclass(Base, pd.DataFrame)):
#    pass


#for name, indexer in indexers():          # Calls pandas machinery
#    setattr(DataFrame, name, None)           # Need to unreference existing indexer
#    DataFrame._create_indexer(name, indexer) # Prior to instantiation new indexer
