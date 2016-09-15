# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Configuration
############################
The configuration file (**~/.exa/config**) has the following structure:

.. code-block:: text

    [paths]
    data: Path to the data directory (default ~/.exa/data)
    notebooks: Path to the notebooks directory (default ~/.exa/notebooks)

    [logging]
    nlogs: Number of log files to rotate (default 3)
    nbytes: Max log file size (in bytes, default 10 MiB)
    syslog: System log file path (default ~/.exa/sys.log)
    dblog: Database log file path (if necessary, default ~/.exa/db.log)
    level: Logging level, 0: warnings, 1: info, 2: debug

    [db]
    uri: String URI for database connection

The configuration file is can be updated manually:

.. code-block:: Python

    exa._config.config['log']['nlogs'] = '4'
    #exa._config.save()

Note that the value must be a string and will be saved on exit or if called
manually (as commented out in the example). If multiple **exa** processes are running
simultaneously (e.g. multiple Jupyter notebooks or Python interpreter consoles)
the last one to exit will write the final configuration file. Automatic saving
can be unregistered if necessary:

.. code-block:: Python

    exa._config.atexit.unregister(exa._config.save)

Finally only edit the configuration file manually when no **exa** (Python) processes
are running or make sure to unregister all automatic saving prior to editing.

Logging
###############
By default **exa** provides two loggers, **db** and **sys**. Both are accessible via
the loggers attribute. The system log is records all messages related to container,
editor, and workflow actions. The database log keeps track of all content
management actions.

Attributes:
    config (:class:`~configparser.ConfigParser`): Framework configuration
    loggers (dict): Dictionary of loggers
    engine (:class:`~sqlalchemy.engine.base.Engine`): Sqlalchemy database engine
"""
import os
import sys
import atexit
import platform
import configparser
import shutil
import logging
import pandas as pd
from textwrap import wrap
from itertools import product
from sqlalchemy import create_engine
from logging.handlers import RotatingFileHandler
from exa._version import __version__


class LogFormat(logging.Formatter):
    """
    Custom logging format for systematic, parsable, and human readable log files.
    """
    spacing = '                                     '
    log_basic = '%(asctime)19s - %(levelname)8s'
    debug_format = """%(asctime)19s - %(levelname)8s - %(pathname)s:%(lineno)d
                                     %(message)s"""
    info_format = """%(asctime)19s - %(levelname)8s - %(message)s"""
    log_formats = {logging.DEBUG: debug_format, logging.INFO: info_format,
                   logging.WARNING: info_format, logging.ERROR: debug_format,
                   logging.CRITICAL: debug_format}

    def format(self, record):
        """
        Overwrites the built-in format function (called when sending a message
        to the logger) with the specific format defined by this class.
        """
        fmt = logging.Formatter(self.log_formats[record.levelno])
        j = '\n' + self.spacing
        record.msg = j.join(wrap(record.msg, width=80))
        return fmt.format(record)


def mkdir(path):
    """
    Create a directory on disk (supports Python 2 and 3). No exception is raised
    if the directory already exists.
    """
    try:    # This approach supports Python 2 and Python 3
        os.makedirs(path)
    except OSError:
        pass


def print_config(out=sys.stdout):
    """
    Display the complete configuration (read-only).
    """
    out.write("(exa {})\n\n\n".format(__version__))
    for name, section in config.items():
        out.write(u"[{}]\n".format(name))
        for key, value in section.items():
            out.write(key + u" = " + value + u"\n")
        out.write(u"\n")


def create_logger(name):
    """
    Construct a custom logger with rotating file handlers and custom format.
    """
    def head(n=10, out=sys.stdout):
        # Custom head function that we attach to the logging.Logger class
        with open(config["logging"][name], 'r') as f:
            lines = u"".join(f.readlines()[:n])
        out.write(lines)

    def tail(n=10, out=sys.stdout):
        # Custom tail function that we attach to the logging.Logger class
        with open(config["logging"][name], 'r') as f:
            lines = u"".join(f.readlines()[-n:])
        out.write(lines)

    logging.basicConfig()
    root = logging.getLogger()
    map(root.removeHandler, root.handlers[:])
    map(root.removeFilter, root.filters[:])
    kwargs = {'maxBytes': int(config['logging']['nbytes']),
              'backupCount': int(config['logging']['nlogs'])}
    handler = logging.handlers.RotatingFileHandler(config['logging'][name], **kwargs)
    handler.setFormatter(LogFormat())
    handler.setLevel(logging.WARNING)
    n = "sqlalchemy.engine.base.Engine" if name == "dblog" else name
    logger = logging.getLogger(n)
    logger.setLevel(logging.WARNING)
    logger.head = head
    logger.tail = tail
    if config['logging']['level'] == '1':
        logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
    elif config['logging']['level'] == '2':
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


@atexit.register
def save():
    """
    Save the configuration file to disk (occurs automatically on exit).

    Warning:
        To ensure that changes to the configuration persist, only alter the
        configuration from one instance of exa, or by hand when exa has not
        been imported.
    """
    config_file = config['dynamic']['config_file']
    del config['dynamic']    # Delete dynamically assigned configuration options
    with open(config_file, "w") as f:
        config.write(f)


def reconfigure(rootname=".exa"):
    """
    Read in the configuration (or generate a new configuration) and set the
    dynamic configuration for the current session.
    """
    global config, engine, loggers
    # Get exa"s root directory (e.g. /home/[username]/.exa, C:\\Users\[username]\\.exa)
    home = os.getenv("USERPROFILE") if platform.system().lower() == "windows" else os.getenv("HOME")
    root = os.path.join(home, rootname)
    mkdir(root)
    # Check for existing config or build one anew
    config_file = os.path.join(root, "config")
    init_flag = False
    if os.path.exists(config_file) and rootname == ".exa":
        stats = os.stat(config_file)
        if stats.st_size > 180:      # Check that the file size > 180 bytes
            config.read(config_file)
    else:
        # paths
        config['paths'] = {}
        config['paths']['data'] = os.path.join(root, "data")
        config['paths']['notebooks'] = os.path.join(root, "notebooks")
        mkdir(config['paths']['data'])
        mkdir(config['paths']['notebooks'])
        # logging
        config['logging'] = {}
        config['logging']['nlogs'] = "3"
        config['logging']['nbytes'] = str(10*1024*1024)    # 10 MiB
        config['logging']['syslog'] = os.path.join(root, "sys.log")
        config['logging']['dblog'] = os.path.join(root, "db.log")
        config['logging']['level'] = "0"
        # db
        config['db'] = {}
        config['db']['uri'] = "sqlite:///" + os.path.join(root, "exa.sqlite")
        init_flag = True
    # Get the dynamic (system/installation/dev dependent) configuration
    config['dynamic'] = {}
    config['dynamic']['root'] = root
    config['dynamic']['home'] = home
    config['dynamic']['config_file'] = config_file
    config['dynamic']['pkg'] = os.path.dirname(os.path.realpath(__file__))
    config['dynamic']['data'] = os.path.join(config['dynamic']['pkg'], "..", "data")
    config['dynamic']['examples'] = os.path.join(config['dynamic']['pkg'], "..", "examples")
    config['dynamic']['numba'] = "false"
    config['dynamic']['cuda'] = "false"
    config['dynamic']['notebook'] = "false"
    try:
        import numba
        config['dynamic']['numba'] = "true"
    except ImportError:
        pass
    try:
        from numba import cuda
        if len(cuda.devices.gpus) > 0:
            config['dynamic']['cuda'] = "true"
    except (AttributeError, ImportError):
        pass
    try:
        cfg = get_ipython().config
        if "IPKernelApp" in cfg:
            config['dynamic']['notebook'] = "true"
    except NameError:
        pass
    # Database engine
    try:
        engine.dispose()
    except AttributeError:
        pass
    engine = create_engine(config['db']['uri'], echo=False)
    # Loggers
    for name in config["logging"].keys():
        if name.endswith("log"):
            loggers[name.replace("log", "")] = create_logger(name)
    if init_flag:
        initialize()    # Inject static data into the database


def initialize():
    """
    Copy tutorial.ipynb to the notebooks directory and update static db data.
    """
    tut = "tutorial.ipynb"
    tutorial_source = os.path.join(config['dynamic']['examples'], tut)
    tutorial_dest = os.path.join(config['paths']['notebooks'], tut)
    shutil.copy(tutorial_source, tutorial_dest)
    # Load isotope static data (replacing existing data)
    isotopes = os.path.join(config['dynamic']['data'], "isotopes.json")
    df = pd.read_json(isotopes, orient='values')
    df.columns = ('A', 'Z', 'af', 'eaf', 'color', 'radius', 'gfactor', 'mass',
                  'emass', 'name', 'eneg', 'quadmom', 'spin', 'symbol', 'szuid',
                  'strid')
    df.index.names = ['pkid']
    df.reset_index(inplace=True)
    df.to_sql(name='isotope', con=engine, index=False, if_exists='replace')
    # Compute and load unit conversions
    path = os.path.join(config['dynamic']['data'], "units.json")
    df = pd.read_json(path)
    for column in df.columns:
        series = df[column].dropna()
        values = series.values
        labels = series.index
        n = len(values)
        factor = (values.reshape(1, n) / values.reshape(n, 1)).ravel()
        from_unit, to_unit = zip(*product(labels, labels))
        df_to_save = pd.DataFrame.from_dict({'from_unit': from_unit,
                                             'to_unit': to_unit,
                                             'factor': factor})
        df_to_save['pkid'] = df_to_save.index
        df_to_save.to_sql(name=column, con=engine, index=False, if_exists='replace')
    # Load physical constants
    path = os.path.join(config['dynamic']['data'], "constants.json")
    df = pd.read_json(path)
    df.reset_index(inplace=True)
    df.columns = ['symbol', 'value']
    df['pkid'] = df.index
    df.to_sql(name='constant', con=engine, index=False, if_exists='replace')


# Create the config, db engine, and loggers
logging.basicConfig()
config = configparser.ConfigParser()
engine = None
loggers = {}
reconfigure()
