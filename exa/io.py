# -*- coding: utf-8 -*-
'''
Object Based Disk IO
===============================================
This module controls reading and writing physical file objects represented
by :class:`~exa.relational.file.File` (database entry) objects and collected
by :class:`~exa.relational.container.Container` objects.

See Also:
    :class:`~exa.relational.container.Container` and
    :class:`~exa.relational.file.File`
'''
from exa.relational import Container, File
from exa.relational.base import event


@event.listens_for(Container, 'before_insert')
def before_insert(mapper, connection, container):
    '''
    Writes files to disk.

    This event listens for the moment just before a
    :class:`~exa.relational.container.Container` entry is inserted into the
    database and is responsible for preparing the associated file entry
    objects, as well performing disk IO.

    See Also:
        :func:`~exa.relational.container.after_insert`
    '''


@event.listens_for(Container, 'after_insert')
def after_insert(mapper, connection, container):
    '''
    Checks that written file's :class:`~exa.relational.file.File` entries are
    correct; if any errors occurred during commit, files on disk are removed
    (to prevent being orphaned) and an exception is raised.
    '''
    print('now we rewrite any hdf5 and other files on disk')

@event.listens_for(Container, 'before_update')
def _before_update(mapper, connection, container):
    '''
    Actions to perform just before commiting Containers
    '''
    print('just before update')

@event.listens_for(Container, 'after_update')
def _update_files(mapper, connection, container):
    '''
    '''
    print('update!')

@event.listens_for(Container, 'after_delete')
def _delete_files(mapper, connection, container):
    '''
    Delete files on disk (represented by entries in the File
    table/instances of the File class) that are associated with the
    recently deleted Container.
    '''
    print('now we delete any hdf5 and other files on disk')
