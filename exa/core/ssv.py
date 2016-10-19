# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Generic CSV Support
######################
Provides an editor with convenience methods tailored specifically for comma
separated value (CSV) files and tab separated value (TSV) files.
"""
import csv
import pandas as pd
from io import StringIO
from exa.core.editor import Editor


class CSV(Editor):
    """
    A convenience class for manipulating CSV (or CSV like, including tab, space,
    etc. separated) files on disk.
    """
    def to_frame(self):
        """
        Create a :class:`~exa.numerical.DataFrame` from this file.
        """
        if self.header:
            return pd.read_csv(StringIO(str(self)), sep=self.delimiter, names=self[0])
        return pd.read_csv(StringIO(str(self)), sep=self.delimiter)

    def __init__(self, *args, **kwargs):
        super(CSV, self).__init__(*args, **kwargs)
        self.remove_blank_lines()
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(self._lines[1])
        self.header = sniffer.has_header(str(self))
        self.delimiter = dialect.delimiter
        self.quoting = dialect.quoting
        self.escapechar = dialect.escapechar
        self.quotechar = dialect.quotechar
