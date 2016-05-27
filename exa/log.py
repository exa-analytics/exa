# -*- coding: utf-8 -*-
'''
Logging
=====================
This module provides three main log files, system, user, and database ('log_sys',
'log_user', and 'log_db'). These files may be inspected interactively:

.. code-block:: Python

    exa.logfiles()             # default: ['log_sys', 'log_user', 'log_db']
    exa.log_head('log_sys')    # prints the head of the system log
    exa.log_tail('log_user')   # prints the tail of the user log

- system: logs automatic messages performed by exa and its sub-packages
- user: logs (non personally identifiable) user actions
- database: logs database interactions
'''
import os
import logging
from logging.handlers import RotatingFileHandler
from textwrap import wrap
from exa import global_config


loggers = {}


class LogFormat(logging.Formatter):
    '''
    Systematic log formatting (for all logging levels).
    '''
    spacing = '                                     '
    log_basic = '%(asctime)19s - %(levelname)8s'
    debug_format = '''%(asctime)19s - %(levelname)8s - %(pathname)s:%(lineno)d
                                     %(message)s'''
    info_format = '''%(asctime)19s - %(levelname)8s - %(message)s'''
    log_formats = {logging.DEBUG: debug_format, logging.INFO: info_format,
                   logging.WARNING: info_format, logging.ERROR: debug_format,
                   logging.CRITICAL: debug_format}
    def format(self, record):
        fmt = logging.Formatter(self.log_formats[record.levelno])
        j = '\n' + self.spacing
        record.msg = j.join(wrap(record.msg, width=80))
        return fmt.format(record)


def logfiles():
    '''
    Lists available log names.

    Returns:
        names (list): List of available log names
    '''
    return [handler.name for handler in logging.root.handlers]


def get_logger(which):
    '''
    Get a log file handler ('sys', 'db', 'user').
    '''
    return loggers[which]


def log_head(log='log_sys', n=10):
    '''
    Print the oldest log messages.

    Args:
        log (str): Log name
        n (int): Number of lines to print
    '''
    print_log(log, n, True)


def log_tail(log='sys', n=10):
    '''
    Print the most recent log messages.

    Args:
        log (str): Log name
        n (int): Number of lines to print
    '''
    print_log(log, n, False)


def print_log(log, n, head=True):
    lines = None
    with open(global_config['log_' + log], 'r') as f:
        lines = f.read().splitlines()
    if head:
        print('\n'.join(lines[:n]))
    else:
        print('\n'.join(lines[-n:]))


def cleanup():
    '''
    Clean up logging file handlers.
    '''
    for name, logger in loggers.items():
        for handler in logger.handlers:
            handler.close()
        logger.handlers = []


def setup_loggers():
    '''
    Setup up loggers and (corresponding) file handlers.
    '''
    global loggers
    cleanup()
    log_files = dict((key, value) for key, value in global_config.items() if key.startswith('log_'))
    for key, path in log_files.items():
        logger = logging.getLogger('sqlalchemy') if 'db' in key else logging.getLogger(key)
        handler = RotatingFileHandler(path, maxBytes=global_config['logfile_max_bytes'],
                                      backupCount=global_config['logfile_max_count'])
        handler.setFormatter(LogFormat())
        logger.addHandler(handler)
        if global_config['exa_persistent'] and global_config['runlevel'] == 0:
            logger.setLevel(logging.WARNING)
        elif global_config['runlevel'] == 1:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.DEBUG)
        loggers[key.replace('log_', '')] = logger


setup_loggers()
