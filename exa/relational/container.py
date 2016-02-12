# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
import traitlets
from ipywidgets import DOMWidget
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from exa import _sys as sys
from exa import _pd as pd
from exa import _np as np
from exa.frames import DataFrame, Updater, ManyToMany
from exa.relational.base import Column, Integer, Base, Name, HexUID, Time, Disk, Meta


ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class ContainerMeta(traitlets.MetaHasTraits, Meta):
    '''
    '''
    pass


class Container(DOMWidget, Name, HexUID, Time, Disk, Base, metaclass=ContainerMeta):
    '''
    Containers control data manipulation, processing, and provide convenient
    visualizations.
    '''
    __slots__ = ['meta']
    # Relational information
    container_type = Column(String(16))
    files = relationship('File', secondary=ContainerFile, backref='containers', cascade='all, delete')
    __mapper_args__ = {
        'polymorphic_identity': 'container',   # This allows the container to
        'polymorphic_on': container_type,      # be inherited.
        'with_polymorphic': '*'
    }
    __dfclasses__ = {}

    # Widget information
    _ipy_disp = DOMWidget._ipython_display_
    _view_module = traitlets.Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = traitlets.Unicode('ContainerView').tag(sync=True)
    width = traitlets.Integer(800).tag(sync=True)
    height = traitlets.Integer(500).tag(sync=True)
    _gui_width = traitlets.Integer(250).tag(sync=True)
    _fps = traitlets.Integer(24).tag(sync=True)

    def to_archive(self, path):
        '''
        Export this container to an archive that can be imported in another
        session (on any machine).
        '''
        raise NotImplementedError()

    def copy(self):
        '''
        Create a copy of the current object
        '''
        cls = self.__class__
        dfs = self.get_dataframes()
        special = self.__dfclasses__.keys()
        kwargs = {'dfs': {}}
        for name, df in dfs.items():               # Subclasses of DataFrame are
            dfcls = df.__class__
            if name in special:                    # passed as individual kwargs
                name = name[1:] if name.startswith('_') else name
                if df is None:
                    kwargs[name] = dfcls()
                else:
                    kwargs[name] = dfcls(df.copy())
            else:
                kwargs['dfs'][name] = dfcls(df.copy())
        kwargs['name'] = self.name                 # All other table attributes (e.g. times)
        kwargs['description'] = self.description   # will be populated automatically
        meta = self.meta                           # Add a note about the copy
        meta['__copy_note__'] = 'copy of container with pkid: {0}'.format(self.pkid)
        kwargs['meta'] = meta
        return cls(**kwargs)

    def info(self):
        '''
        Get (human readable) information about the container.
        '''
        n = self.nbytes()
        sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'too high..']
        for size in sizes:
            s = str(n).split('.')
            if len(s) > 1:
                if len(s[0]) <= 3 and len(s[1]) > 3:
                    print('size ({0}): {1}'.format(size, n))
                    break
            elif len(s[0]) <= 3:
                print('size ({0}): {1}'.format(size, n))
                break
            n /= 1024

    def nbytes(self):
        '''
        Compute the size of the current object in bytes.
        '''
        csum = 0
        for trait in self._trait_values.values():
            csum += sys.getsizeof(trait)
        for df in self.get_dataframes().values():
            if df is not None:
                csum += df.values.nbytes
                csum += df.index.nbytes
                csum += df.columns.nbytes
        return csum

    def get_dataframes(self):
        '''
        Get a dictionary of dataframes. Keys are the dataframe variable name
        and values are the dataframe itself.
        '''
        return {name: getattr(self, name) for name in self.__dfclasses__.keys()}
        #return {name: obj for name, obj in vars(self).items() if isinstance(obj, DataFrame) or isinstance(obj, Updater) or isinstance(obj, ManyToMany)}

    @classmethod
    def from_archive(cls, path):
        '''
        Import a container from an archive into the current session.

        Note:
            This function will also create file entries and objects
            corresponding to the data provided in the archive.
        '''
        raise NotImplementedError()

    def _update_traits(self):
        '''
        Overwritten when containers require complexe trait updating logic.
        '''
        self._update_df_traits()

    def _add_unicode_traits(self, **values):
        '''
        Add custom traits from DataFrame json strings.

        Warning:
            Only supports Unicode!
        '''
        for name, value in values.items():
            obj = traitlets.Unicode().tag(sync=True)
            obj.class_init(self.__class__, name)
            setattr(self.__class__, name, obj)
            obj.instance_init(self)
            self[name] = value
            self.send_state(name)

    def _update_df_traits(self):
        '''
        '''
        for name in self.__dfclasses__.keys():
            value = self[name]
            if isinstance(value, DataFrame):
                values = self[name].get_trait_values()
                self._add_unicode_traits(**values)

    def _handle_custom_msg(self, *args, **kwargs):
        '''
        Recieve and dispatch messages from the JavaScript frontend to the
        Python backend.
        '''
        print(args)
        print(kwargs)

    def _ipython_display_(self):
        '''
        Custom HTML representation
        '''
        self._ipy_disp()
        print(repr(self))

    def _repr_html_(self):
        return self._ipython_display_()

    def _get_by_index(self, index):
        '''
        Positional getter.
        '''
        cp = self.copy()
        for name, df in cp.get_dataframes().items():
            if isinstance(df, DataFrame):
                cp[name] = df._get_by_index(index)
        #cp._update_traits()
        return cp

    def _get_by_indices(self, indices):
        '''
        '''
        cp = self.copy()
        for name, df in cp.get_dataframes().items():
            if isinstance(df, DataFrame):
                cp[name] = df._get_by_indices(indices)
        #cp._update_traits()
        return cp

    def _get_by_slice(self, key):
        '''
        '''
        cp = self.copy()
        for name, df in cp.get_dataframes().items():
            if isinstance(df, DataFrame):
                cp[name] = df._get_by_slice(key)
        #cp._update_traits()
        return cp

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __getitem__(self, key):
        '''
        Integers, slices, and lists are assumed to be values in the index (
        for multi-indexed dataframes, corresponding to level 0).
        '''
        if isinstance(key, int):
            return self._get_by_index(key)
        elif isinstance(key, list):
            return self._get_by_indices(key)
        elif isinstance(key, slice):
            return self._get_by_slice(key)
        elif isinstance(key, str):
            return getattr(self, key)
        else:
            raise NotImplementedError()

    def __setitem__(self, key, value):
        '''
        Custom set calls __setattr__ to enforce certain types.
        '''
        setattr(self, key, value)

    def __setattr__(self, key, value):
        '''
        Custom attribute setting to enforce custom dataframe types.
        '''
        if isinstance(value, pd.DataFrame) and not isinstance(value, DataFrame):
            for name, cls in self.__dfclasses__.items():
                if key == name:
                    super().__setattr__(key, cls(value))
                    return
            super().__setattr__(key, DataFrame(value))
            return
        super().__setattr__(key, value)

    def __init__(self, meta=None, dfs=None, **kwargs):
        super().__init__(**kwargs)
        if dfs:                               # DataFrame attributes
            if isinstance(dfs, dict):
                for name, df in dfs.items():
                    setattr(self, name, df)
                    self.__dfclasses__[name] = df.__class__
            else:
                raise TypeError('Argument "dfs" must be of type dict.')
        self.meta = meta

    def __repr__(self):
        c = self.__class__.__name__
        p = self.pkid
        n = self.name
        u = self.hexuid
        return '{0}({1}: {2}[{3}])'.format(c, p, n, u)

    def __str__(self):
        return repr(self)


def concat(containers, axis=0, join='inner'):
    '''
    Concatenate a collection of containers.
    '''
    raise NotImplementedError()
