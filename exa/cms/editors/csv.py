# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Generic CSV Support
######################
Provides an editor with convenience methods tailored specifically for comma
separated value (CSV) files.
"""
import re
import pandas as pd
from io import StringIO
from exa.cms.editors.editor import Editor


class CSV(Editor):
    """
    A convenience class for manipulating CSV (or CSV like) files on disk.
    """
    def clean(self):
        """
        Remove extra whitespace, and replace commonly used null characters with
        nothing.
        """
        self.replace('*', ' ')

    def to_frame(self):
        """
        Create a :class:`~exa.numerical.DataFrame` from this file.
        """
        return pd.read_csv(StringIO(str(self)))

    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)
        self.remove_blank_lines()    # Remove blank lines
        # Attempt to determine the separator and delimter
        line1 = str(self[1].strip())
        # Determine the delimiter and separator
        # Determine if a header exists
        line0 = str(self[0]).strip()
        if line0.startswith("#"):
            pass

        # Determine the internal separator and delimiter

        # Now determine the internal separator, delimiter
