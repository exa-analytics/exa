# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data container
####################################
An in-memory related data container.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx
from traitlets import Unicode, Dict

import exa
from exa import Base
from exa.core.data import Data

class Box(Base):
    name = Unicode(help="string name of container")
    meta = Dict(help="metadata dictionary")
    description = Unicode(help="container description")

    def copy(self, **kws):
        return self.__class__(**kws)

    def slice(self, key):
        pass

    def groupby(self):
        pass

    def info(self):
        pass

    def memory(self):
        pass

    def network(self):
        pass

    def save(self, name=None, directory=None, parquet_backend='pyarrow'):
        """Save a bundle of files to a tarball."""
        name = name or self.hexuid
        directory = Path(directory) or exa.cfg.savedir
        bundle = directory / name
        bundle.mkdir(parents=True, exist_ok=True)
        for data in self._data.values():
            data.save(bundle)

    def load(self):
        pass

    def from_hdf(cls):
        # Do we opt for parquet+pickle?
        # Maybe easier/cleaner than HDF
        pass

    def __delitem__(self, key):
        if key in self._data:
            del self._data[key]

    def __getitem__(self, key):
        pass

    def __init__(self, name=None, description=None, meta=None, **kwargs):
        self.log.info('adding {} attrs'.format(len(kwargs)))
        self._data = {}
        for key, value in kwargs.items():
            if isinstance(value, Data):
                self._data[key] = value
            setattr(self, key, value)
        self.name = name
        self.description = description
        self.meta = meta
        self.hexuid = uuid4().hex
