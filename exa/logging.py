# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Logging
############
By default exa provides two loggers, "db" and "sys". Both are accessible via the
loggers attribute. The system log is records all messages related to container,
editor, and workflow actions. The database log keeps track of all content
management actions (it is used when a 3rd party database logging solution is not
used).

Attributes:
    loggers (dict): Available loggers for use (defaults: "db" and "sys")
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from textwrap import wrap
from exa._config import config


class LogFormat(logging.Formatter):
    """
    Custom log format used by all loggers.
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


def _create_logger(name):
    """
    Create a logger with a given name.
    """
    def head(n=10):
        # Custom head function that we attach to the logging.Logger class
        with open(config["LOGGING"][name], 'r') as f:
            lines = "".join(f.readlines()[:n])
        print(lines)
    def tail(n=10):
        # Custom tail function that we attach to the logging.Logger class
        with open(config["LOGGING"][name], 'r') as f:
            lines = "".join(f.readlines()[-n:])
        print(lines)
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    handler = RotatingFileHandler(config['LOGGING'][name],
                                  maxBytes=int(config['LOGGING']['nbytes']),
                                  backupCount=int(config['LOGGING']['nlogs']))
    handler.setFormatter(LogFormat())
    logger.addHandler(handler)
    logger.head = head
    logger.tail = tail
    if config['LOGGING']['level'] == '1':
        logger.setLevel(logging.INFO)
    elif config['LOGGING']['level'] == '2':
        logger.setLevel(logging.NOTSET)
    return logger


loggers = {}
for name in config["LOGGING"].keys():
    if name.endswith("log"):
        loggers[name.replace("log", "")] = _create_logger(name)

#def setup_loggers():
#    """
#    Setup up loggers and (corresponding) file handlers.
#    """
#    global config
#    if 'loggers' in config:
#        cleanup()
#    config['loggers'] = {}
#    log_files = dict((key, value) for key, value in config.items() if key.startswith('log_'))
#    for key, path in log_files.items():
#        logger = logging.getLogger('sqlalchemy') if 'db' in key else logging.getLogger(key)
#        handler = RotatingFileHandler(path, maxBytes=config['logfile_max_bytes'],
#                                      backupCount=config['logfile_max_count'])
#        handler.setFormatter(LogFormat())
#        logger.addHandler(handler)
#        if config['runlevel'] == 0:
#            logger.setLevel(logging.WARNING)
#        elif config['runlevel'] == 1:
#            logger.setLevel(logging.INFO)
#        else:
#            logger.setLevel(logging.DEBUG)
#        config['loggers'][key.replace('log_', '')] = logger
#
#
#def logfiles():
#    """
#    Lists available log names.
#
#    Returns:
#        names (list): List of available log names
#    """
#    return [handler.name for handler in logging.root.handlers]
#
#
#def get_logger(which='sys'):
#    """
#    Get a log file handler ('sys', 'db', 'user').
#    """
#    return config['loggers'][which]
#
#
#def head(log='log_sys', n=10):
#    """
#    Print the oldest log messages.
#
#    Args:
#        log (str): Log name
#        n (int): Number of lines to print
#    """
#    print_log(log, n, True)
#
#
#def tail(log='sys', n=10):
#    """
#    Print the most recent log messages.
#
#    Args:
#        log (str): Log name
#        n (int): Number of lines to print
#    """
#    print_log(log, n, False)
#
#
#def print_log(log, n, head=True):
#    """
#    Print the head or tail of a given log file (see :func:`~exa.log.head`
#    and :func:`~exa.log.tail`).
#    """
#    lines = None
#    with open(config['log_' + log], 'r') as f:
#        lines = f.read().splitlines()
#    if head:
#        print('\n'.join(lines[:n]))
#    else:
#        print('\n'.join(lines[-n:]))
#
#
#def cleanup():
#    """
#    Clean up logging file handlers.
#    """
#    for name, logger in config['loggers'].items():
#        for handler in logger.handlers:
#            handler.close()
#        logger.handlers = []
#    del config['loggers']
#
