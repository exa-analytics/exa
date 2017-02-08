# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Management Functionality
##################################################
The content management system requires initialization functions and features
which are provided by this module.
"""
from glob import glob
from exa import _config
from exa.cms.base import Base, scoped_session
from exa.cms.files import File


def init_db():
    """Initialize CMS tables."""
    Base.metadata.create_all(_config.engine)


def init_tutorial():
    """Create the tutorial notebook."""
    for fp in glob(_config.config['paths']['notebooks'] + "/*.ipynb"):
        with scoped_session() as session:
            tutorial = File.from_path(fp)
            session.add(tutorial)


if 'init_cms' in _config.config['dynamic']:
    init_db()
    init_tutorial()
