# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Core objects include the :class:`~exa.core.editor.Editor`,
:class:`~exa.core.parser.Sections`, :class:`~exa.core.parser.Parser`,
:class:`~exa.core.composer.Composer`, and :class:`~exa.core.container.Container`.
Additional objects provided by the ``core`` sub-package include
:class:`~exa.core.dataframe.DataFrame`, used to create standardized `Pandas`_
like dataframes.
"""
from .dataframe import DataFrame, Feature
from .container import Container
from .editor import Editor
from .parser import Sections, Parser
from .composer import Composer
