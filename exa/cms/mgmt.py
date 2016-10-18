# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Database Management
##################################################
Database table creation and database inspection is provided by this module.
"""
import os
import blaze as bz
import pandas as pd
from exa._config import config, engine
from exa.cms.base import Base, scoped_session
from exa.cms.files import File


def tables():
    """Display all tables."""
    return db.fields

def tail(table, n=10, to_frame=False):
    """
    Extract the end of a table.

    Args:
        n (int): Number of entries to extract
        to_frame (bool): Return a dataframe (default false)

    Returns:
        sliced: Blaze data object or pandas dataframe
    """
    sliced = db[table].sort().tail(n)
    if to_frame:
        return bz.odo(sliced, pd.DataFrame)
    return sliced


def init_cms():
    """Initialize CMS tables."""
    fp = os.path.join(config['paths']['notebooks'], 'tutorial.ipynb')
    if not os.path.exists(fp):
        raise FileNotFoundError("Missing tutorial.ipynb at {}".format(fp))
    Base.metadata.create_all(engine)
    with scoped_session() as session:
        tutorial = File.from_path(fp)
        session.add(tutorial)


def init_db_interface():
    """(Re)initialize the database interface."""
    global db
    db = bz.Data(engine)


if 'init_cms' in config['dynamic']:
    init_cms()
db = None
init_db_interface()
