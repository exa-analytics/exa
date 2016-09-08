# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Configuration
########################
This module generates the "~/.exa" directory where all databases, logs, notebooks,
and data reside by default.

[PATHS]
data: Path to the data directory (default ~/.exa/data)
notebooks: Path to the notebooks directory (default ~/.exa/notebooks)

[LOGGING]
nlogs: Number of log files to rotate
nbytes: Max log file size (in bytes)
syslog: System log file path
dblog: Database log file path (if necessary)
level: Logging level, 0: normal, 1: extra info, 2: debug

[DB]
uri: String URI for database connection
"""
import os
import sys
import atexit
import platform
import configparser
import shutil


@atexit.register
def save():
    """
    Save the configuration file to disk (occurs automatically on exit).

    Warning:
        To ensure that changes to the configuration persist, only alter the
        configuration from one instance of exa, or by hand when exa has not
        been imported.
    """
    del config["dynamic"]    # Delete dynamically assigned configuration options
    with open(config_file, "w") as f:
        config.write(f)


def mkdir(path):
    """
    Safely create a directory.
    """
    try:    # This approach supports Python 2 and Python 3
        os.makedirs(path)
    except OSError:
        pass


def init():
    """
    Copy tutorial.ipynb to the notebooks directory and update static DB data.
    """
    tut = "tutorial.ipynb"
    tutorial_source = os.path.join(config["dynamic"]["pkg"], "..", "examples", tut)
    tutorial_dest = os.path.join(config["PATHS"]["notebooks"], tut)
    shutil.copy(tutorial_source, tutorial_dest)


# The following sets up the configuration variable, config
config = configparser.ConfigParser()
# Get exa"s root directory (e.g. /home/[username]/.exa, C:\\Users\[username]\\.exa)
home = os.getenv("USERPROFILE") if platform.system().lower() == "windows" else os.getenv("HOME")
root = os.path.join(home, ".exa")
mkdir(root)
# Check for existing config or build one anew
config_file = os.path.join(root, "config")
if os.path.exists(config_file):
    stats = os.stat(config_file)
    if stats.st_size > 180:      # Check that the file size > 180 bytes
        config.read(config_file)
else:
    # PATHS
    config["PATHS"] = {}
    config["PATHS"]["data"] = os.path.join(root, "data")
    config["PATHS"]["notebooks"] = os.path.join(root, "notebooks")
    mkdir(config["PATHS"]["data"])
    mkdir(config["PATHS"]["notebooks"])
    # LOGGING
    config["LOGGING"] = {}
    config["LOGGING"]["nlogs"] = "3"
    config["LOGGING"]["nbytes"] = str(10*1024*1024)    # 10 MiB
    config["LOGGING"]["syslog"] = "sys.log"
    config["LOGGING"]["dblog"] = "db.log"
    config["LOGGING"]["level"] = "0"
    # DB
    config["DB"] = {}
    config["DB"]["uri"] = "sqlite:///" + os.path.join(root, "exa.sqplite")
# Finally set up some dynamic ("live") parameters
config["dynamic"] = {}
config["dynamic"]["pkg"] = os.path.abspath(__file__)
config["dynamic"]["root"] = root
config["dynamic"]["numba"] = "false"
config["dynamic"]["cuda"] = "false"
config["dynamic"]["notebook"] = "false"
try:
    import numba
    config["dynamic"]["numba"] = "true"
except ImportError:
    pass
try:
    from numba import cuda
    if len(cuda.devices.gpus) > 0:
        config["dynamic"]["cuda"] = "true"
except (AttributeError, ImportError):
    pass
try:
    cfg = get_ipython().config
    if "IPKernelApp" in cfg:
        config["dynamic"]["notebook"] = "true"
except NameError:
    pass
