# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Generic CSV Support
######################
Provides an editor with convenience methods tailored specifically for comma
separated value (CSV) files and tab separated value (TSV) files.
"""
import csv
from exa.core.editor import Editor


class SSV(Editor):
    """
    A convenience class for manipulating CSV (or CSV like, including tab, space,
    etc. separated) files on disk.
    """
    def to_dataobj(self, skipinitialspace=True, **kwargs):
        """
        Create a data object from the file.

        Args:
            kwargs: See below

        Returns:
            dataobj: A dataframe containing the data

        Note:
            A list of keyword arguments can be found at
            http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
        """
        if self.header:
            names = self._lines[0].split(self.delimiter)
            return pd.read_csv(self.to_stream(), sep=self.delimiter, names=names,
                               skipinitialspace=skipinitialspace, **kwargs)
        return super(SSV, self).to_dataobj(skipinitialspace=skipinitialspace, **kwargs)

    def __init__(self, *args, **kwargs):
        super(SSV, self).__init__(*args, **kwargs)
        self.remove_blank_lines()
        sniffer = csv.Sniffer()
        sample = "\n".join(self._lines[1:10])
        dialect = sniffer.sniff(sample)
        self.header = None
        self.delimiter = dialect.delimiter
        self.quoting = dialect.quoting
        self.escapechar = dialect.escapechar
        self.quotechar = dialect.quotechar
        self.ncols = len(sample.split("\n")[0].split(self.delimiter))
        if sniffer.has_header(sample):
            self.header = self._lines[0].split(dialect.delimiter)
