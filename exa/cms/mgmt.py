# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Database Management
##################################################
Initialize the database and add the tutorial notebooks to the exa directory.

TODO blaze compat example
"""
import os
from exa import _config
from exa.cms.base import Base, scoped_session
from exa.cms.files import File


def init_db():
    """Initialize CMS tables."""
    Base.metadata.create_all(_config.engine)


def init_tutorial():
    """Create the tutorial notebook."""
    fp = os.path.join(_config.config['paths']['notebooks'], 'exa_tutorial.ipynb')
    with scoped_session() as session:
        tutorial = File.from_path(fp)
        session.add(tutorial)


if 'init_cms' in _config.config['dynamic']:
    init_db()
    init_tutorial()
