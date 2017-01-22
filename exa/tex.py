# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
TeX Utilities
#############################
Functions to provide additional support for writing data to `LaTeX`_ format.

.. _LaTeX: https://www.latex-project.org/about/
"""
def cleanup_pandas(string):
    """Cleanup output of :func:`~pandas.DataFrame.to_latex`."""
    string = string.replace("textbackslash", "")
    string = string.replace("\\textasciicircum", "^")
    string = string.replace("\\{", "{")
    string = string.replace("\\}", "}")
    string = string.replace("\\_", "_")
    string = string.replace("\\^", "^")
    string = string.replace("\\$", "$")
    return string
