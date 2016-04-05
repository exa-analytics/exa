# -*- coding: utf-8 -*-
'''
Logging
=====================
'''
import os
import logging
from logging.handlers import RotatingFileHandler
from textwrap import wrap
from exa import _conf


class _LogFormat(logging.Formatter):
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


def get_logfile_path(name):
    '''
    Get the log file path for the log with the given name.
    '''
    for log_file in log_files:
        if name in log_file:
            return log_files[log_file]


def log_names():
    '''
    Lists available log names.

    Returns:
        names (list): List of available log names
    '''
    return [handler.name for handler in logging.handlers]


def log_head(log='log_sys', n=10):
    '''
    Print the oldest log messages.

    Args:
        log (str): Log name
        n (int): Number of lines to print
    '''
    _print_log(log, n, True)


def log_tail(log='log_sys', n=10):
    '''
    Print the most recent log messages.

    Args:
        log (str): Log name
        n (int): Number of lines to print
    '''
    _print_log(log, n, False)


def _print_log(log, n, head=True):
    lines = None
    with open(_conf[log], 'r') as f:
        lines = f.read().splitlines()
    if head:
        print('\n'.join(lines[:n]))
    else:
        print('\n'.join(lines[-n:]))


def _cleanup():
    '''
    Clean up logging file handlers.
    '''
    _remove_handlers()


def _remove_handlers():
    '''
    Clean up logging file handlers.
    '''
    handlers = logging.root.handlers[:]
    for handler in handlers:
        handler.close()
        logging.root.removeHandler(handler)


log_files = dict((key, value) for key, value in _conf.items() if key.startswith('log_'))
_remove_handlers()
# Add custom handlers
for i, (key, path) in enumerate(log_files.items()):
    handler = RotatingFileHandler(path, maxBytes=_conf['logfile_max_bytes'],
                                  backupCount=_conf['logfile_max_count'])
    handler.setFormatter(_LogFormat())
    logging.root.addHandler(handler)
    logging.root.handlers[i].setLevel(logging.DEBUG)
    logging.root.handlers[i].set_name(key)
