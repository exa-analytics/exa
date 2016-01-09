# -*- coding: utf-8 -*-
'''
Logging
=====================
'''
import logging
from textwrap import wrap
from exa import _os as os
from exa.config import Config


class _LogFormat(logging.Formatter):
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


log_files = {
    'system': Config.syslog,
    'test': Config.testlog,
    'user': Config.userlog
}


loggers = {
    'system': logging.getLogger('system'),
    'test': logging.getLogger('test'),
    'user': logging.getLogger('user')
}


def setup():
    '''
    Should only be called on package import. Sets up logging style
    for the rest of the package.
    '''
    for handler in logging.root.handlers:     # Remove default handlers
        logging.root.removeHandler(handler)
    for name, path in log_files.items():
        handler = logging.handlers.RotatingFileHandler(
            path,
            maxBytes=Config.maxlogbytes,
            backupCount=Config.maxlogcount
        )
        handler.setFormatter(_LogFormat())
        loggers[name].addHandler(handler)
        loggers[name].setLevel(logging.DEBUG)


def get_logger(name='system'):
    '''
    Get one of the loggers available to exa.

    Args:
        name (str): One of ['system', 'test', 'user']

    Returns:
        logger (:class:`~logging.Logger`): Logging object
    '''
    if name in loggers:
        return loggers[name]
    else:
        raise KeyError('Unknown logger name')


def log_tail(log='sys', n=10):
    '''
    Displays the most recent messages of the specified log file.

    Args
        log (str): One of ['sys', 'rel', 'doc', 'num', 'unit']
        n (int): Number of lines to display
    '''
    _show_log(log, n)


def log_head(log='sys', n=10):
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
