# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exceptions
#################################
Exa exceptions enable static or dynamic messages using a convenient API. The
class level attribute 'default' is used to define the messages. If this attribute
is callable (i.e. it is a function) then any arguments to the exception are
passed to this function. If the 'default' attribute is not callable then the
static message it contains is simply displayed.

.. code-block:: Python

    # Static error
    class MyException(ExaException):
        default = "This is a static message"
    raise MyException()
    # Prints MyException("This is a static message")

    # Simple callable default
    class OtherException(ExaException):
        default = "This is a dynamic message {}!".format
    raise OtherException("Hello World")
    # Prints OtherException("This is a dynamic message Hello World!")

    # The default attribute may be a more complex function too
    class ComplexException(ExaException):
        @staticmethod
        def default(arg0, arg1, kwarg=None):
            # Complex logic to determine dynamic message
            return "properly formatted string based on args and kwargs"

For logging purposes a keyword argument can also be passed to any Exa
exception specifying the log level (e.g. MyException(level='info').

See Also:
    See :mod:`~exa._config` for supported logging levels.
"""
from exa._config import loggers


logger = loggers['sys']


class ExaException(Exception):
    """
    Exa exceptions have a default message that can be static or dynamic.
    The class level 'default' attribute is a static string or callable
    function that returns the error message. When raising an Exa exception,
    pass a level='loglevel' keyword argument to log the result (the default
    log level is info).
    """
    default = "None"

    def __init__(self, *args, **kwargs):
        level = kwargs.pop('level', 'info')
        msg = kwargs.pop('msg', self.default)
        if callable(msg):    # Note that "callable" may not always be around
            msg = msg(*args, **kwargs)
        super(ExaException, self).__init__(msg)
        if level == 'info':
            logger.info(msg)
        elif level == 'warn':
            logger.warn(msg)
        elif level == 'error':
            logger.error(msg)
        elif level == 'critical':
            logger.critical(msg)
        else:
            logger.debug(msg)


class TypeConversionError(ExaException, TypeError):
    """
    Raised when casting an object as a given type fails.

    See Also:
        For context and use see :mod:`~exa.typed`.

    Note:
        This exception is also a TypeError.
    """
    @staticmethod
    def default(obj, totype):
        msg = 'Type conversion failed for "{}" with type {} to type {}.'
        fromtype = type(obj)
        return msg.format(obj, fromtype, totype)
