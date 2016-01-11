# -*- coding: utf-8 -*-
'''
Exceptions, Errors, and Warnings
==================================
All base level exceptions are defined here.
'''
from exa import _re as re
from exa.decorators import logger


@logger
class ExaException(Exception):
    '''
    Base exa exception. Provides simple templating for systematic exception,
    error, and warning message styles.
    '''
    def __init__(self, msg=None, log=True):
        spacer = '\n' + ' ' * len(self.__class__.__name__) + '  '    # Align the message
        if msg is None:
            msg = self.msg
        else:
            msg = re.sub(r'\s*\n\s*', spacer, msg)
        super().__init__(msg)
        if log:
            self._logger.error(msg)


class ContainerError(ExaException):
    '''
    Raised when a container is not properly constructed. Containers are required
    to have the attribute "frame" (:class:`~pandas.DataFrame`) containing a
    "count" column that corresponds to the number of objects in each frame.
    An object can be anything: stock ids, particles, atoms, potatoes.

    .. code-block:: Python

        import pandas as pd
        frame = pd.DataFrame({'count': 0}, index=[0])    # Single frame with no objects
        container = exa.Container(frame=frame)
        container.frame    # Displays the frame dataframe
    '''
    msg = '''Containers require an attribute "frame" containing at a minimum
        the count of objects in the frame - the column "count" must exist in
        this dataframe!'''


class UnsupportedFileType(ExaException):
    '''
    Raised when an unexpected filetype is given as an argument.
    '''
    _msg = '''Unsupported file type "{0}".'''

    def __init__(self, ftype):
        self.msg = self._msg.format(ftype)
        super().__init__()


class MissingProgramError(ExaException):
    '''
    Raised when attempting to add an object to a :class:`~exa.relational.Program`
    before the Program entry has been created in the database.
    '''
    msg = 'Please create a Program (exa.Program(...)) first'


class MissingProjectError(ExaException):
    '''
    Raised when attempting to add an object to a :class:`~exa.relational.Project`
    before the Project entry has been created in the database.
    '''
    msg = 'Please create a Project (exa.Project(...)) first'


class MissingJobError(ExaException):
    '''
    Raised when attempting to add an object to a :class:`~exa.relational.Job`
    before the Job entry has been created in the database.
    '''
    msg = 'Please create a Job (exa.Job(...)) first'
