# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data container
####################################
An in-memory related data container.
"""
import os
import uuid
import tarfile
from pathlib import Path

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

    def copy(self, *args, **kws):
        """Copy the box and all its Data. All args and kwargs
        are forwarded to the underlying Data.data().copy()
        method and assumes a deepcopy for each Data.

        Warning:
            If dataset is large, may impact performance.
            Are you sure you need a copy?
        """
        copy = {}
        for name, data in self._data.items():
            # TODO : expose Data.copy args, kwargs?
            copy[name] = data.copy(*args, **kws)
        return self.__class__(**copy)

    def slice(self, key):
        pass

    def groupby(self):
        pass

    def info(self):
        info = []
        for name, data in self._data.items():
            df = data.data()
            # TODO: prepend __module__?
            if isinstance(df, pd.DataFrame):
                info.append((name, type(data), df.memory_usage().sum(), df.shape))
            elif isinstance(df, pd.Series):
                info.append((name, type(data), df.memory_usage(), df.shape))
            else:
                info.append((name, type(data), None, None))
        info = pd.DataFrame(info, columns=['name', 'type', 'size', 'shape'])
        return info.set_index('name').sort_index()

    def memory(self):
        pass

    def network(self):
        """Build a network of the relationships between
        data as specified by the container's metadata.
        """
        # TODO: log-scale sizes for nodes
        sizes = self.info()['size'].to_dict()
        # TODO: there is a bug in this
        related = {}
        print("name0, name1, index0, data1.indexes, data1.columns")
        for name0, data0 in self._data.items():
            for name1, data1 in self._data.items():
                if data0 is data1:
                    continue
                for index0 in data0.indexes:
                    print(name0, name1, index0, data1.indexes, data1.columns)
                    if index0 in data1.indexes:
                        related[(name0, name1)] = 'index-index'
                        related[(name1, name0)] = 'index-index'
                    for col1 in data1.columns:
                        print(col1, index0, col1.startswith(index0))
                        if col1.startswith(index0):
                            related[(name0, name1)] = 'index-column'
                            related[(name1, name0)] = 'column-index'
                            print(related)
        g = nx.Graph()
        g.add_nodes_from(sizes.keys())
        g.add_edges_from(related.keys())
        g.edge_types = related
        return g

    def save(self, name=None, directory=None):
        """Save a bundle of files to a tarball. Not sure
        how parquet will interact with tarfile buffer so
        taking the easy way out for now."""
        # TODO : box needs to additionally save its
        #        own metadata like Data
        name = name or self.hexuid
        adir = exa.cfg.savedir
        if directory is not None:
            adir = Path(directory)
        bundle = adir / name
        bundle.mkdir(parents=True, exist_ok=True)
        for data in self._data.values():
            data.save(directory=bundle)
        tarfl = (adir / name).as_posix() + '.tar.gz'
        with tarfile.open(tarfl, 'w:gz') as tar:
            for fl in bundle.iterdir():
                tar.add(fl)
                fl.unlink()
        bundle.rmdir()
        return tarfl

    def load(self, name, directory=None):
        """Load a Container from a tar.gz created by the
        save method."""
        # TODO : box needs to additionally load its
        #        own metadata like Data
        adir = exa.cfg.savedir
        if directory is not None:
            adir = Path(directory)
        contents = {}
        tarfl = (adir / name).as_posix() + '.tar.gz'
        with tarfile.open(tarfl, 'r:gz') as tar:
            for info in tar:
                _, fl = os.path.split(info.name)
                name, xt = os.path.splitext(fl)
                contents.setdefault(name, {})
                contents[name][xt.strip('.')] = tar.extractfile(info)
            for name, buffers in contents.items():
                data = exa.Data.from_tarball(**buffers)
                self._data[data.name] = data
                setattr(self, data.name, data)

    # TODO : should __setitem__ inspect for Data and add to _data?

    def __delitem__(self, key):
        if key in self._data:
            del self._data[key]

    def __getitem__(self, key):
        pass

    def __init__(self, *args, hexuid=None, **kwargs):
        self._data = {}
        for key, value in kwargs.items():
            if isinstance(value, Data):
                self._data[key] = value
            setattr(self, key, value)
        self.log.info('added {} attrs'.format(len(self._data)))
        super().__init__(*args, **{
            k: v for k, v in kwargs.items()
            if k not in self._data
        })
        self.hexuid = hexuid or uuid.uuid4().hex
