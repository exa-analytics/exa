# -*- coding: utf-8 -*-
'''
Editor
====================================
Text-editor-like functionality for programatically manipulating raw text input
and output files. Supports commonly used logic such as (simple or regular
expression) replacement, insertion, and deletion.
'''
import re
from io import StringIO
from exa import _os as os
from exa.utility import mkpath


class Editor:
    '''
    An editor is the contents of a text file that can be programmatically
    manipulated.

    .. code-block:: Python

        from exa.editor import Editor
        template = "Hello World!\\nHello {user}"
        editor = Editor.from_template(template)
        print(editor[0])                             # "Hello World!"
        print(editor.format(user='Bob'))             # "Hello World!\nHello Bob"
        print(len(editor))                           # 2
        del editor[0]                                # Deletes first line
        print(len(editor))                           # 1
        editor.write(fullpath=None, user='Alice')    # "Hello Alice"
    '''
    def write(self, fullpath=None, *args, **kwargs):
        '''
        Write the editor's contents to disk.

        Optional arguments can be used to format the editor's contents. If no
        file path is given, prints to standard output (useful for debugging).

        Args:
            fullpath (str): Full file path, if no path given will write to stdout (default)
            *args: Positional arguments to format the editor with
            **kwargs: Keyword arguments to format the editor with

        See Also:
            :func:`~exa.editor.Editor.format`
        '''
        if fullpath is None:
            if self.filename:
                fullpath = self.filename
        if fullpath:
            with open(fullpath, 'w') as f:
                f.write(str(self).format(*args, **kwargs))
        else:
            print(str(self).format(*args, **kwargs))

    def format(self, inplace=False, *args, **kwargs):
        '''
        Format the string representation of the editor.

        Args:
            inplace (bool): If True, overwrite editor's contents with formatted contents
        '''
        if inplace:
            self._lines = str(self).format(*args, **kwargs).splitlines()
        else:
            return str(self).format(*args, **kwargs)

    def head(self, n=10):
        '''
        Display the top of the file.

        Args:
            n (int): Number of lines to display
        '''
        r = self.__repr__().split('\n')
        print('\n'.join(r[:n]), end=' ')

    def tail(self, n=10):
        '''
        Display the bottom of the file.

        Args:
            n (int): Number of lines to display
        '''
        r = self.__repr__().split('\n')
        print('\n'.join(r[-n:]), end=' ')

    def append(self, lines):
        '''
        Args:
            lines (list): List of line strings to append to the end of the editor
        '''
        raise NotImplementedError()

    def preappend(self, lines):
        '''
        Args:
            lines (list): List of line strings to insert at the beginning of the editor
        '''
        raise NotImplementedError()

    def insert(self, lines={}):
        '''
        Note:
            To insert before the first line, use 0; to insert after the last
            line use :func:`~exa.editor.Editor.append`.

        Args:
            lines (dict): Line number key, line string value dictionary to insert
        '''
        pass

    def delete_blank(self):
        '''
        Permanently removes blank lines from input.
        '''
        to_remove = []
        for i, line in enumerate(self):
            ln = line.strip()
            if ln == '':
                to_remove.append(i)
        self.del_lines(to_remove)

    def delete(lines):
        '''
        Delete the given line numbers.

        Args:
            lines (list): List of integers corresponding to lines to delete
        '''
        for k, i in enumerate(lines):
            del self[i - k]

    @property
    def variables(self):
        '''
        Display a list of templatable variables present in the file.

        Templating is accomplished by creating a bracketed object in the same
        way that Python performs `string formatting`_. The editor is able to
        replace the placeholder value of the template. Integer templates are
        positional arguments.

        .. _string formatting: https://docs.python.org/3.6/library/string.html
        '''
        string = str(self)
        constants = [match[1:-1] for match in re.findall('{{[A-z0-9]}}', string)]
        variables = re.findall('{[A-z0-9]*}', string)
        return sorted(set(variables).difference(constants))

    @property
    def meta(self):
        '''
        Generate a dictionary of metadata (default is string text of editor).
        '''
        return {'filename': self.filename}

    @classmethod
    def from_file(cls, path):
        '''
        Create an editor instance from a file on disk.
        '''
        filename = os.path.basename(path)
        lines = lines_from_file(path)
        return cls(lines, filename)

    @classmethod
    def from_stream(cls, f):
        '''
        Create an editor instance from a file stream.
        '''
        lines = lines_from_stream(f)
        filename = f.name if hasattr(f, 'name') else None
        return cls(lines, filename)

    @classmethod
    def from_string(cls, string):
        '''
        Create an editor instance from a string template.
        '''
        return cls(lines_from_string(string))

    def __init__(self, data, filename=None):
        '''
        Args:
            data: File path, stream, or string text
            filename: Name of file or None
        '''
        self.filename = filename
        if os.path.isfile(data):
            self._lines = lines_from_file(data)
            self.filename = os.path.basename(data)
        elif isinstance(data, StringIO):
            self._lines = lines_from_stream(data)
            self.filename = data.name if hasattr(data, 'name') else None
        elif isinstance(data, str):
            self._lines = lines_from_string(data)
        elif isinstance(data, list):
            self._lines = data
        else:
            raise TypeError('Unknown type for arg data: {}'.format(type(data)))

    def __delitem__(self, line):
        del self._lines[line]     # "line" is the line number minus one

    def __getitem__(self, line):
        return self._lines[line]

    def __setitem__(self, line, value):
        self._lines[line] = value

    def __iter__(self):
        for line in self._lines:
            yield line

    def __len__(self):
        return len(self._lines)

    def __str__(self):
        return '\n'.join(self._lines)

    def __repr__(self):
        r = None
        fmt = '{0}: {1}\n'
        n = len(str(len(self)))
        for i, line in enumerate(self):
            ln = str(i).rjust(n, ' ')
            if r is None:
                r = fmt.format(ln, line)
            else:
                r += fmt.format(ln, line)
        return r


def lines_from_file(path):
    '''
    Line list from file.
    '''
    lines = None
    with open(path) as f:
        lines = f.read().splitlines()
    return lines

def lines_from_stream(f):
    '''
    Line list from an IO stream.
    '''
    return f.read().splitlines()

def lines_from_string(string):
    '''
    Line list from string.
    '''
    return string.splitlines()
