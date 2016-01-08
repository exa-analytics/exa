# -*- coding: utf-8 -*-
'''
Logging
=====================
'''
import os
import logging
from textwrap import wrap
from exa.config import Config


class Format(logging.Formatter):
    '''
    Systematic log formatting (for all logging levels).
    '''
    log_basic = '%(asctime)19s - %(levelname)8s'
    debug_format = '''%(asctime)19s - %(levelname)8s - %(pathname)s:%(lineno)d
                                     %(message)s'''
    info_format = '''%(asctime)19s - %(levelname)8s - %(message)s'''
    spacing = '                                     '
    log_formats = {logging.DEBUG: debug_format, logging.INFO: info_format,
                   logging.WARNING: info_format, logging.ERROR: debug_format,
                   logging.CRITICAL: debug_format}

    def format(self, record):
        fmt = logging.Formatter(self.log_formats[record.levelno])
        j = '\n' + self.spacing
        record.msg = j.join(wrap(record.msg, width=80))
        return fmt.format(record)


Format = Format()
loggers = {'system': logging.getLogger('system'),
           'doctest': logging.getLogger('doctest'),
           'unittest': logging.getLogger('unittest'),
           'relational': logging.getLogger('relational'),
           'numerical': logging.getLogger('numerical')}


def setup():
    '''
    Should only be called on package import. Sets up logging style
    for the rest of the package.
    '''
    # Remove default handlers
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    logs = {'system': Config.syslog,
            'doctest': Config.doclog,
            'unittest': Config.unitlog,
            'relational': Config.rellog,
            'numerical': Config.numlog}
    lvl = logging.DEBUG if Config.developer else logging.INFO
    # Check that files exist
    for key, logfile in logs.items():
        if not os.path.isfile(logfile):
            with open(logfile, 'w') as f:
                f.write('\n')
    # Clean up old logs
    for logger, filepath in logs.items():
        mode = 'a'
        if float(os.path.getsize(filepath)) > Config.maxlogsize:
            mode = 'w'
        handler = logging.FileHandler(filepath, mode=mode)
        handler.setFormatter(Format)
        loggers[logger].addHandler(handler)
        loggers[logger].setLevel(lvl)


def get_logger(name='system'):
    '''
    Get one of the loggers available to exa.

    Args:
        name (str): One of ['system', 'doctest', 'unittest', 'relational', 'numerical']

    Returns:
        logger (:class:`~logging.Logger`): Logger object
    '''
    if name in loggers:
        return loggers[name]
    else:
        raise KeyError('Unknown logger name')


def tail(log='sys', n=10):
    '''
    Displays the most recent messages of the specified log file.

    Args
        log (str): One of ['sys', 'rel', 'doc', 'num', 'unit']
        n (int): Number of lines to display
    '''
    _show_log(log, n)


def head(log='sys', n=10):
    '''
    Displays the earliest messages of the specified log file.

    Args
        log (str): One of ['sys', 'rel', 'doc', 'num', 'unit']
        n (int): Number of lines to display
    '''
    _show_log(log, n, True)


def _show_log(log, n, head=False):
    '''
    See Also:
        This function is called by :func:`~exa.log.head` and
        :func:`~exa.log.tail`, not usually called directly.
    '''
    lines = None
    with open(Config[log + 'log'], 'r') as f:
        lines = f.readlines()
    if head:
        print('\n'.join(lines[:n]))
    else:
        print('\n'.join(lines[-n:]))
