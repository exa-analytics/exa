# -*- coding: utf-8 -*-
'''
Editor
====================================
Text-editor-like functionality for programatically manipulating raw text input
and output files.
'''


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
    @property
    def meta(self):
        '''
        Generate a dictionary of metadata (default is string text of editor).
        '''
        return {'text': str(self)}

    def write(self, fullpath=None, *args, **kwargs):
        '''
        Write the editor's contents to disk.

        Optional arguments can be used to format the editor's contents.

        Args:
            fullpath (str): Full file path
        '''
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

    def remove_blank_lines(self):
        '''
        Permanently removes blank lines from input.
        '''
        to_remove = []
        for i, line in enumerate(self):
            ln = line.strip()
            if ln == '':
                to_remove.append(i)
        self.del_lines(to_remove)

    def del_lines(lines):
        '''
        Delete the given line numbers.

        Args:
            lines (list): List of integers corresponding to lines to delete
        '''
        for k, i in enumerate(lines):
            del self[i - k]

    @classmethod
    def from_file(cls, path):
        '''
        Create an editor instance from a file on disk.
        '''
        lines = None
        with open(path) as f:
            lines = f.read().splitlines()
        return cls(lines)

    @classmethod
    def from_stream(cls, f):
        '''
        Create an editor instance from a file stream.
        '''
        lines = f.read().splitlines()
        return cls(lines)

    @classmethod
    def from_template(cls, template):
        '''
        Create an editor instance from a string template.
        '''
        lines = template.splitlines()
        print(lines)
        return cls(lines)

    def __delitem__(self, key):
        del self._lines[key]

    def __getitem__(self, key):
        return self._lines[key]

    def __setitem__(self, key, value):
        self._lines[key] = value

    def __iter__(self):
        for line in self._lines:
            yield line

    def __len__(self):
        return len(self._lines)

    def __init__(self, lines):
        self._lines = lines

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
