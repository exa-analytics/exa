# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Text Utilities
#############################
Text and `LaTeX`_ processing. Functions provided by this module make use of
module level attributes which can be modified as needed.

.. code-block:: python

    exa.tex.cleaners.append(("pattern", "replacement"))
    fixed = exa.tex.cleanup_pandas(text)

Attributes:
    cleaners (list): List of replacements commonly needed for pandas objects

.. _LaTeX: https://www.latex-project.org/about/
"""
import re
import copy


cleaners = [("textbackslash", ""), ("\\textasciicircum", "^"), ("\\{", "{"),
           ("\\}", "}"), ("\\_", "_"), ("\\^", "^"), ("\\$", "$")]


def cleanup_pandas(text):
    """
    Cleanup output of pandas `to_latex`_.

    Typically the output text of a call to the pandas function ``to_latex``,
    where the pandas object contains, for example, math text or other special
    characters become mangled. This function cleans many common issues up.

    Args:
        text (str): Text with bad characters

    Returns:
        modtext (str): Cleaned text

    .. _to_latex: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_latex.html#pandas.DataFrame.to_latex
    """
    for pat, rep in cleaners:
        text = text.replace(pat, rep)
    return text


def constant_decimals(text, n):
    """
    Make the number of decimals shown systematic.

    For visual purposes it is occasionally useful to be able to append arbitrary
    zeros to numerical data (where it doesn't imply incorrect accuracy).

    Args:
        text (str): Text containing floating point numbers
        n (int): Number of decimal places desired

    Returns:
        modtext (str): Modified text
    """
    cptext = copy.copy(text)
    for item in re.findall('\.\d{1,}', cptext):
        new = copy.copy(item.strip())
        if len(new) > n:
            new = new[:n+1]   # +1 accounts for the '.'
        else:
            new += '0'*(n - len(new) + 1)
        new += " "
        text = text.replace(item, new)
    return text


def text_value_cleaner(text):
    """Clean and convert string value to Python numeric type."""
    text = text.strip()
    if "." in text:
        try:
            text = float(text)
        except ValueError:
            pass
    else:
        try:
            text = int(text)
        except ValueError:
            pass
    return text