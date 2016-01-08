# -*- coding: utf-8 -*-
'''
Container
=======================
A :class:`~exa.container.Container` is the fundamental object for manipulating
data. It supports both batch data (e.g. loading data from csv files on disk)
and data streams (e.g. live data retrieval via HTTP). Although it is possible
to use this class directly, it is typically inherited by a data specific
container to enhance usability and take advantage of data specific functions.

Note
    The :class:`~exa.container.Container` is also the backbone object that
    connects the Python backend with the JavaScript frontend.
'''
from exa import DOMWidget, Int, Unicode
from exa import Config


class Container(DOMWidget):
    '''
    Abstract object for interaction with ndarray data and metadata.

    Containers provide a set of utilities for data organization and exploration.
    They can be specific to a type of data object or generic with support for any
    dimensionality of data.

    The container on disk is represented by multiple files. The two standard files,
    required to save/load or import/export are:
    - HDF5 for dataframe storage   (ndarray data: frame, one, two, etc.)
    - yml for metadata storage     (non-ndarray data: ids, names, descriptions, etc.)
    Auxiliary files are stored in a labeled folder.
    '''
    # Definitions
    _view_module = Unicode('nbextensions/exa/exa.container', sync=True)
    _view_name = Unicode('ContainerView', sync=True)
    _jslog = Unicode(Config.jslog, sync=True)
    _orient = Unicode('values', sync=True)    # pandas to_json orientation
    name = Unicode(sync=True, allow_none=True)
    description = Unicode(sync=True, allow_none=True)
    _cid = Int(sync=True, allow_none=True)    # Container id

    # Properties
    @property
    def df_dict(self):
        '''
        Collect all attached dataframes into a single object.

        Returns
            dfs (dict): Dictionary of attached dataframes (name as key)
        '''
        return dict([(k, v) for k, v in self.__dict__.items() if isinstance(v, pd.DataFrame)])

    # Public methods
    def save(self, export_to=None):
        '''
        Save the current container and all associated data.

        If an entry for the container does not exist, it will be created. Containers
        can store a number of different objects, including static images, text files,
        and other objects, all of which will be saved in the appropriate on disk
        structure (internally). If the container is being exported, it will be saved
        as an archive to be transported and loaded externally.

        Args:
            export_to (str): Save to specified location (to be loaded elsewhere)
        '''
        if self._cid is None:
            print('Create new entry!')
        else:
            print('Update entry/entries')
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    # Private methods
    def _update_view(self):
        '''
        Update the javascript view.
        '''
        pass

    def _update_data(self):
        '''
        Update the pandas dataframes.
        '''
        pass

    def _set_dataframe(self, key, value):
        '''
        Attaches a :class:`~pandas.DataFrame` to a container.
        '''
        name = '_' + key
        setattr(self, key, value)
        self.add_traits(**{name: Unicode(value.to_json(orient=self._orient))})

    def _get_str(key):
        '''
        Select an attribute of the container by string.

        Args:
            key (str): String name of attribute to select

        Returns:
            item: Selected item
        '''
        return self.__dict__[key]

    def _get_int(key):
        '''
        Select a single data object from a container.

        Data containers may contain logically organized subcontainers. Often this
        occurs when dealing with time data (e.g. the concept of frames in a
        :class:`~exa.atomic.container.Universe`).

        Args:
            key (int): Value of the base index (of all attached dataframes) to select by

        Returns:
            container: Container of source type
        '''
        raise NotImplementedError()

    def _repr_html_(self):
        if self._view_needs_update == False:
            return self._update_view()
        self._ipython_display_()

    # Internal methods
    def __getitem__(self, key):
        '''
        Decides what type of getter is needed based on the type of the key.
        '''
        if isinstance(key, str):
            return self._get_str(key)
        elif isinstance(key, int):
            return self._get_items_by_int(key)
        raise NotImplementedError()

    def __setitem__(self, name, value):
        '''
        Setting an attribute on a container object also means creation
        of a json representation of the
        '''
        if isinstance(value, pd.DataFrame):
            raise NotImplementedError()
        raise NotImplementedError()

    def __iter__(self):
        '''
        '''
        raise NotImplementedError()

    def __len__(self):
        '''
        '''
        raise NotImplementedError()

    def __add__(self):
        '''
        '''
        raise NotImplementedError()

    def __sub__(self):
        raise NotImplementedError()

    def __mul__(self):
        raise NotImplementedError()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)

    def __init__(self, name=None, description=None, cid=None, **dfkwargs):
        super().__init__()
        self.name = name
        self.description = description
        self._cid = cid
        for dfname, df in dfkwargs.items():
            self._set_dataframe(dfname, df)












#from exa import pd, Project, Job, File, display, yaml, Loader, Dumper, Config
#from exa.utils import mkpath
#from exa.errors import ContainerError
#
#
#PATHS = {'containers': Config.containers,
#         'keys': Config.keys,
#         'auxiliary': Config.auxiliary}
#SYS = Config.system
#
#
## Certain functions may need to be called exa.container.concat(args)
## or containerobj.concat(othercontainer). Keeping the concat function
## here allows for both API's to be used.
#def concat(objs, axis=0, join='inner'):
#    '''
#    Concatenate a collection of container objects into a single container.
#
#    Args
#        objs: List or tuple of containers to concatenate
#        axis (int): Axis on which to concatenate objects (0: index, 1: columns)
#        join (str): Innerlap concat ('inner') or outerlap concat ('outer')
#
#    Returns
#        container: Concatenated container with new indices
#
#    Warning
#        This function will reset all indices! This may cause a loss in fidelity
#        of data origin! Furthermore, projects, jobs, and files do not survive
#        concatenation!
#    '''
#    raise NotImplementedError()
#
#
#def _getitem_from_df(df, slicer):
#    '''
#    Slices out sections of a dataframe in a user intuitive way.
#    '''
#    def many(df, ndims, slicers, cols):
#        '''
#        '''
#        if cols == []:
#            cols = slice(None)
#        while len(slicers) < ndims:
#            slicers.append(slice(None))
#        slicers = tuple(slicers)
#        return df.loc[idx[slicers], idx[cols]].copy()
#
#    def single(df, slicer):
#        '''
#        '''
#        return df.loc[slicer].copy()
#
#    ndims = len(df.index.names)    # Number of dimensions
#    if isinstance(slicer, slice):
#        if ndims > 1:
#            return many(df, ndims, [slicer], slice(None))
#        else:
#            return single(df, slicer)
#    elif isinstance(slicer, tuple):
#        if ndims > 1:
#            slicers = []
#            cols = []
#            for obj in slicer:
#                if isinstance(obj, slice) or isinstance(obj, tuple):
#                    slicers.append(obj)
#                elif isinstance(obj, list):
#                    cols += obj
#                else:
#                    cols.append(obj)
#            return many(df, ndims, slicers, cols)
#        else:
#            return single(df, slicer)
#    return single(df, slicer)
#
#
#def _extract_by_indices(**kwargs):
#    '''
#    Advanced extraction of a "sub"-container from the master container
#    '''
#    raise NotImplementedError()
#
#
#class Container:
#    '''
#    Fundamental object for manipulation of static or streaming data.
#
#
#    Base object for organizing data on which analytics will be performed. Every container must
#    have a data table attribute called "frame" that contains (at a minimum) the count of objects
#    in each frame.
#
#    .. code-block:: Python
#
#        import pandas as pd
#        frame = pd.DataFrame({'count': 0}, index=[0])    # Single frame with no objects
#        container = exa.Container(frame=frame)
#        container.frame    # Displays the frame dataframe
#
#    Attributes
#        frame (:class:`~pandas.DataFrame`): The only required dataframe (see above)
#        name (str): Container name (optional)
#        description (str): Description of container (optional)
#        metadata (dict): Dictionary of information about the work (key, value pairs - optional)
#        project: An instance of a :class:`~exa.relational.Project` or kwargs used to create a new project (optional)
#        job: An instance of a :class:`~exa.relational.Job` or kwargs used to create a new job (optional)
#        hdf5_file: An instance of a :class:`~exa.relational.File` or kwargs used to create a new file (optional)
#        meta_file: An instance of a :class:`~exa.relational.File` or kwargs used to create a new file (optional)
#    '''
#    # The _KEYS attribute keeps track of the (standardized) attribute names
#    _KEYS = ['frame', 'name', 'description', 'project', 'job', 'metadata',
#             'hdf5_file', 'meta_file']
#
#    # Normal bound methods
#    def save(self, name=None, description=None, hdf5_file=None, meta_file=None):
#        '''
#        Save the container to disk for quick reload. The container will be saved as an HDF5 file
#        containing all of the dataframes with the keys being the name of the dataframe attribute.
#        A corresponding YAML file (same uid) is created containing all of the information needed
#        to recover the object (in case of database loss).
#
#        Args
#            name (str): Container name (optional)
#            description (str): Container description (optional)
#            hdf5_file: An instance of a :class:`~exa.relational.File` or kwargs used to create a new file (optional)
#            meta_file: An instance of a :class:`~exa.relational.File` or kwargs used to create a new file (optional)
#
#        Warning
#            For disk space reason there is currently no versioning of containers! Saving an existing
#            container will overwrite the file with the new data tables!
#        '''
#        if name is not None:
#            self.name = name
#        if description is not None:
#            self.description = description
#        # Prep
#        if self.hdf5_file is None and self.meta_file is None:
#            # If the file has never been saved, create the file objects automatically
#            self.hdf5_file = File(name=name, description=description, ftype='hdf5')
#            self.meta_file = File(name=name, description=description, ftype='yaml')
#            self.meta_file.uid = self.hdf5_file.uid
#        elif self.hdf5_file is None or self.meta_file is None:
#            # Mismatch in the files?!
#            raise Exception(msg='Mismatch of files, make sure both hdf5_file and meta_file exist!')
#        # Write the HDF5 file
#        store = pd.HDFStore(self.hdf5_path, mode='w', complevel=9, complib='blosc')
#        if SYS == 'windows':
#            store.close()
#            store = pd.HDFStore(self.hdf5_path, mode='w', complevel=9, complib='zlib')
#        for dfname, df in self._dataframes.items():
#            store.put(dfname, df, format='table', data_columns=True)
#        store.close()
#        # Write the meta file (metadata+)
#        data = self.metadata
#        if data is None:
#            data = {}
#        data['keys'] = list(self._dataframes.keys())
#        if self.project is not None:
#            data['project'] = self.project.to_dict()
#        if self.job is not None:
#            data['job'] = self.job.to_dict()
#        with open(self.meta_path, mode='w') as f:
#            yaml.dump(data, stream=f, Dumper=Dumper, default_flow_style=True, allow_unicode=True)
#        # Write the json view file
#        print('Saved!')
#        return None
#
#    # Classmethods
#    @classmethod
#    def load(cls, name_or_id):
#        '''
#        Load a container from a file id. The file name or file id can be given.
#        If multiple names exist, a :class:`NameError` will be raised.
#
#        Args
#            name_or_id: File name or integer id
#
#        Returns
#            container: Properly typed container with all attached attributes
#
#        Raises
#            NameError: If the file cannot be identified by name.
#        '''
#        f = File[name_or_id]
#        files = None
#        if isinstance(f, File):
#            files = File._get_by_uid(f.uid)
#        elif len(f) > 2:
#            raise Exception('''Too many files with this id: {0}!
#                            Can't determine which container to load.
#                            Use id instead.'''.format(name_or_id))
#        else:
#            raise Exception('see alex?')
#        # If we only got a single file (by id) get by uid
#        hdf5_file = None
#        meta_file = None
#        obj = cls(frame=None, loading=True)
#        for f in files:
#            if f.ftype == 'hdf5':
#                obj.hdf5_file = f
#            if f.ftype == 'yaml':
#                obj.meta_file = f
#        # Read in the yaml data
#        meta_data = {}
#        with open(obj.meta_path, 'r') as f:
#            meta_data = yaml.load(f, Loader=Loader)
#        # Populate dataframes
#        if 'keys' in meta_data:
#            for key in meta_data['keys']:
#                setattr(obj, key, pd.read_hdf(obj.hdf5_path, key=key))
#        # Populate yaml data
#        for key, value in meta_data.items():
#            setattr(obj, key, value)
#        obj._update_view()
#        setattr(obj, '_update_view_required', False)
#        print('Loaded!')
#        return obj
#
#    # Properties
#    @property
#    def _view(self):
#        '''
#        '''
#        if self._view_needs_update:
#            self._update_view()
#        return self._widget_view
#
#    @property
#    def framelist(self):
#        '''
#        Generates a list of frame indices.
#
#        Returns
#            frames (list): List of frame indices
#        '''
#        return [int(frame) for frame in self.frame.index.get_level_values('frame')]
#
#    @property
#    def hdf5_path(self):
#        '''
#        Generate the container's hdf5 file path.
#        '''
#        return self._get_path('hdf5')
#
#    @property
#    def meta_path(self):
#        '''
#        Generate the container's meta file path.
#        '''
#        return self._get_path('meta')
#
#    @property
#    def _dataframes(self):
#        '''
#        Get all of the dataframe objects associated with the container.
#
#        Returns
#            dictdfs (dict): Dictionary of dataframe names and dataframes
#        '''
#        return dict([(k, v) for k, v in self.__dict__.items() if isinstance(v, pd.DataFrame)])
#
#    # Private methods
#    def _get_path(self, which):
#        '''
#        '''
#        obj = self[which + '_file']
#        if obj is None:
#            raise Exception()
#        else:
#            return mkpath(PATHS[which], obj.uid)
#
#    def _update_view(self):
#        '''
#        '''
#        self._widget_view = self._widget_class(self)
#        self._view_needs_update = False
#
#    def _get_attribute(self, key):
#        '''
#        Get an attribute by string name.
#        '''
#        return self.__dict__[key]
#
#    def _get_frame(self, frame):
#        '''
#        Get a single frame from the universe (only acts on dataframes,
#        doesn't keep metadata or other objects such as project, job, etc.).
#        '''
#        frame = self.framelist.index(frame)
#        kwargs = {'force_update_view': True}
#        for dfname, df in self._dataframes.items():
#            kwargs[dfname] = df.loc[frame:frame].copy()
#        return self.__class__(**kwargs)
#
#    def _get_frames(self, frames):
#        '''
#        '''
#        #frames = [self.framelist.index(frame) for frame in frames]
#        frames = self.framelist[frames]
#        #if type(frames) is slice:
#        #    frames = self.framelist[frames]
#        #else:
#        #    raise NotImplementedError('See Alex')
#        kwargs = {'force_update_view': True}
#        for dfname, df in self._dataframes.items():
#            kwargs[dfname] = df.loc[frames].copy()
#        return self.__class__(**kwargs)
#
#    # Python built-ins
#    def __getitem__(self, key):
#        '''
#        Fast flexible getter capable of slicing/selecting dataframes
#        as well as attribute selection.
#        '''
#        if isinstance(key, str):
#            return self._get_attribute(key)
#        elif isinstance(key, int):
#            return self._get_frame(key)
#        elif isinstance(key, slice) or isinstance(key, list) or isinstance(key, tuple):
#            return self._get_frames(key)
#        else:
#            raise NotImplementedError('See Alex')
#
#    def __iter__(self):
#        '''
#        Iterate over all frames in the container
#        '''
#        for fdx in self.framelist:
#            yield self[fdx]
#
#    def __len__(self):
#        '''
#        The length of a container is its frame count.
#        '''
#        return len(self.framelist)
#
#    def __init__(self, frame, name=None, description=None, metadata=None,
#                 project=None, job=None, hdf5_file=None, meta_file=None,
#                 loading=False, view=None, widget=None, force_update_view=False,
#                 **kwargs):
#        # Enforce that the frame dataframe contains the count attribute if not "loading"
#        if loading == False:
#            if frame is None:
#                raise ContainerError
#            if 'count' not in frame.columns:
#                raise ContainerError
#        # Public
#        self.frame = frame
#        self.name = name
#        self.description = description
#        self.metadata = metadata
#        self.project = project
#        self.job = job
#        self.hdf5_file = hdf5_file
#        self.meta_file = meta_file
#        # Generate if needed
#        if isinstance(project, dict):
#            self.project = Project(**project)
#        if isinstance(job, dict):
#            self.job = Job(**job)
#        if isinstance(hdf5_file, dict):
#            self.hdf5_file = File(**hdf5_file)
#        if isinstance(meta_file, dict):
#            self.meta_file = File(**meta_file)
#        # Private (for visualization)
#        self._widget_class = widget
#        self._widget_view = view
#        self._view_needs_update = True
#        if force_update_view:
#            self._update_view()
#        for key, value in kwargs.items():
#            if type(value) is pd.DataFrame:
#                setattr(self, key, value)
#
#    def __repr__(self):
#        # Provides a default repr for this container and subclassed containers
#        return '{0}({1})'.format(self.__class__.__name__, len(self))
#
#    def _repr_html_(self):
#        if self._view is None:
#            return display(self.__repr__())
#        else:
#            return display(self._view)
#
