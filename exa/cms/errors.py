# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
CMS Exceptions
#################################
"""
from exa.errors import ExaException


class FileCreationError(ExaException):
    """
    Raised when creating a :class:`~exa.cms.files.File` object from a given
    file on disk.
    """
    def __init__(self, src, dst):
        msg = "Unable to create File object at {} (source {})".format(dst, src)
        super(FileCreationError, self).__init__(msg=msg)
