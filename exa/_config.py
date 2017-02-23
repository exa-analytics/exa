# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Config
############################
Exa uses a configuration file to store some (user editable) settings. The
configuration file follows the `standard`_ format for Python.

.. code-block:: text

    [paths]
    data: Path to the data directory (default ~/.exa/data)
    notebooks: Path to the notebooks directory (default ~/.exa/notebooks)
    scratch: Path to scratch directory (default ~/.exa/tmp)

    [logging]
    nlogs: Number of log files to rotate (default 3)
    nbytes: Max log file size (in bytes, default 10 MiB)
    syslog: System log file path (default ~/.exa/sys.log)
    dblog: Database log file path (if necessary, default ~/.exa/db.log)
    level: Logging level, 0: warnings, 1: info, 2: debug

    [db]
    uri: String URI for database connection

The configuration can be updated during a session, but changes won't take effect
until the following session unless the configuration is saved manually.

.. code-block:: Python

    exa._config.config['log']['nlogs'] = '4'
    # To write the changes immediately
    exa._config.save()

Editing the configuration file 'by hand' can only be done when no Exa sessions
are running (i.e. make sure no Python instances have imported exa). For most
users the default configuration is sufficient.

Tip:
    If needed, automatic function calls can be unregistered to prevent auto-
    updating of the configuration.

    .. code-block:: Python

        exa._config.atexit.unregister(exa._config.save)

Exa's root directory can be set by setting the environment variable 'EXAROOT'.
If set, Exa will look for a configuration in this directory before looking
in the default location (e.g. '~/.exa').


Logging
###############
Exa uses two loggers, one for database logs (``db``) and one for core system logs
(``sys``). Both loggers are accessible via the ``loggers`` attribute but should
not be needed for typical usage.


Database
###############
Lastly, the database engine is established by this module. The database engine
provides a connection to an external or internal database system that manages
the table schemas provided in ``cms`` subpackage. These schemas are primarily
used for tracking user actions and organizing projects, etc. Exa leverages the
rich `PyData`_ stack for connections to external data storage systems.


Attributes:
    config (:class:`~configparser.ConfigParser`): Framework configuration
    loggers (dict): Dictionary of loggers
    engine (:class:`~sqlalchemy.engine.base.Engine`): Sqlalchemy database engine

.. _standard: https://docs.python.org/3/library/configparser.html
.. _PyData: http://pydata.org/
"""
import pandas as pd
import os, sys, atexit, platform, shutil, logging, configparser
from glob import glob
from sqlalchemy import create_engine
from logging.handlers import RotatingFileHandler
from exa._version import __version__
join = os.path.join


# Logging formats
default = logging.Formatter("%(asctime)19s - %(levelname)8s - %(message)s")
info = logging.Formatter("%(asctime)19s - %(levelname)8s - %(name)20s - %(message)s")
debug = logging.Formatter("%(asctime)19s - %(levelname)8s - %(pathname)s:%(lineno)d - %(message)s")
formats = {logging.DEBUG: debug, logging.INFO: info, logging.WARNING: default,
           logging.ERROR: default, logging.CRITICAL: default}


def mkdir(path):
    """Safely create a directory on disk."""
    try:    # This approach supports Python 2 and Python 3
        os.makedirs(path)
    except OSError:
        pass


def info(out=sys.stdout):
    """Display config and other information (read-only)."""
    out.write(u"(exa {})\n\n\n".format(__version__))
    for name, section in config.items():
        out.write(u"[{}]\n".format(name))
        for key, value in section.items():
            out.write(key + u" = " + value + u"\n")
        out.write(u"\n")


def close_logger(logger):
    """Gracefully close a logger."""
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def create_logger(name):
    """Create a modified logger with rotating file handlers."""
    def head(n=10, out=sys.stdout):
        """Show the head of the log."""
        with open(config['logging'][name], 'r') as f:
            lines = u"".join(f.readlines()[:n])
        out.write(lines)

    def tail(n=10, out=sys.stdout):
        """Show the tail of the log."""
        with open(config['logging'][name], 'r') as f:
            lines = u"".join(f.readlines()[-n:])
        out.write(lines)

    kwargs = {'maxBytes': int(config['logging']['nbytes']),
              'backupCount': int(config['logging']['nlogs'])}
    n = "sqlalchemy.engine.base.Engine" if name == "dblog" else name
    logger = logging.getLogger(n)
    handler = RotatingFileHandler(config['logging'][name], **kwargs)
    logger.head = head
    logger.tail = tail
    if config['logging']['level'] == '2':
        handler.setFormatter(debug)
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    elif config['logging']['level'] == '1':
        handler.setFormatter(debug)
        handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
    else:
        handler.setFormatter(default)
        handler.setLevel(logging.WARNING)
        logger.setLevel(logging.WARNING)
    logger.addHandler(handler)
    return logger


@atexit.register
def save(del_dynamic=True):
    """
    Save the configuration file to disk (occurs automatically on exit).

    Warning:
        Setting no_del to true may cause unstable behavior; it is used for
        testing only.
    """
    config_file = join(config['dynamic']['root'], "config.ini")
    if del_dynamic:
        del config['dynamic']    # Delete dynamically assigned config options
    with open(config_file, "w") as f:
        config.write(f)


def reconfigure(test=False):
    """
    Read in the configuration (or generate a new configuration) and set the
    dynamic configuration for the current session.
    """
    # Editing the module level variables
    global config
    global engine
    global loggers
    init = False
    # Determine root directory
    exaroot = os.getenv('EXAROOT')
    home = os.getenv("USERPROFILE") if platform.system().lower() == "windows" else os.getenv("HOME")
    if test == True:
        exaroot = join(home, ".exa_test")
        mkdir(exaroot)
        init = True
    elif exaroot is None:
        exaroot = join(home, ".exa")
        mkdir(exaroot)
    # Set the dynamic configuration
    ipynb = "false"
    try:
        cfg = get_ipython().config
        if "IPKernelApp" in cfg:
            ipynb = "true"
    except NameError:
        pass
    pkg = os.path.dirname(os.path.realpath(__file__))
    docnb = os.path.abspath(join(pkg, "..", "docs/source/notebooks"))
    data = os.path.abspath(join(pkg, "..", "data"))
    config['dynamic'] = {'root': exaroot, 'notebook': ipynb, 'pkg': pkg,
                         'docnb': docnb, 'data': data, 'home': home}
    # Set the default static config
    config['paths'] = {'data': join(exaroot, "data"),
                       'scratch': join(exaroot, "tmp"),
                       'notebooks': join(exaroot, "notebooks")}
    config['logging'] = {'nlogs': "3", 'nbytes': "10485760", 'level': "0",
                         'syslog': join(exaroot, "sys.log"),
                         'dblog': join(exaroot, "db.log")}
    config['db'] = {'uri': "sqlite:///" + join(exaroot, "exa.sqlite")}
    # Update the default static config
    config_file = join(exaroot, "config.ini")
    if os.path.exists(config_file):
        config.read(config_file)
    else:
        # First time importing Exa...
        init = True
        # Create default paths
        for path in config['paths'].values():
            mkdir(path)
    # Create loggers
    for logger in loggers.values():
        close_logger(logger)
    logging.basicConfig()
    root = logging.getLogger()
    map(root.removeHandler, root.handlers[:])
    for name in config['logging'].keys():
        if name.endswith("log"):
            loggers[name.replace("log", "")] = create_logger(name)
    # Update the cms db engine
    try:
        engine.dispose()
    except AttributeError:
        pass
    engine = create_engine(config['db']['uri'], echo=False)
    # Set DB init flag and save initial config
    if init:
        config['dynamic']['init_cms'] = "true"
        save(False)


# Create the config, db engine, and loggers
config = configparser.ConfigParser()
engine = None
loggers = {}
reconfigure()
atexit.register(engine.dispose)
