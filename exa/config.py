# -*- coding: utf-8 -*-
'''
Configuration and Initialization
====================================
Loads the Configuration (if applicable) and instantiates the session.

Attributes:
    username (str): Username (OS level)
    interactive (bool): True if running inside a jupyter notebook environment
    system (str): 'windows', 'linux', 'darwin'
    home (str): User's exa "home" directory (e.g. ~/)
    exa (str): The ".exa" directory (e.g. ~/.exa)
    keys (str): Container key file store (yaml files, ~/.exa/keys)
    containers (str): Container store (hdf5 files, ~/.exa/containers)
    auxiliary (str): Auxiliary data storage (~/.exa/auxiliary)
    static (str): Static data directory
    extensions (str): Jupyter's extensions directory
    html (str): Static HTML directory
    css (str): Static CSS directory
    js (str): Javascript directory
    syslog (str): System log file (e.g. ~/.exa/system.log)
    unitlog (str): Unittest log file (e.g. ~/.exa/unittest.log)
    doclog (str): Doctest log file (e.g. ~/.exa/doctest.log)
    numerical (dict): Parameters (backend, database, host, user)
    relational (dict): See numerical

Note:
    The Configuration class is called "Config" and is not visible in the
    documentation because it is a singleton: the class object instance is
    set to an instance of itself.
'''
import __main__ as _m
import os
import getpass
import platform
import yaml
from notebook.nbextensions import jupyter_data_dir
from exa.utils import mkpath


class Config:
    '''
    The Config class is essentially a dictionary of parameters.
    See the documentation in the module's docstring.
    '''
    _description = '''# exa's Configuration'''

    def save(self):
        '''
        Default save location ~/.exa/config.yml
        '''
        confpath = mkpath(self.exa, 'config.yml')
        with open(confpath, 'w') as f:
            f.write(self._description + '\n\n')
            f.write(yaml.dump(self.__dict__, default_flow_style=False))

    def update(self, other):
        '''
        Custom attribute update method, which doesn't overwrite with None.
        '''
        if other is None:
            pass
        else:
            for k, v in other.items():
                if v is not None:    # Doesn't update if null (None)
                    self[k] = v

    def relational_engine(self):
        '''
        '''
        b = self.relational.backend
        e = self.exa
        d = self.relational.database
        h = self.relational.host
        u = self.relational.user
        if b == 'sqlite':
            return '{0}:///{1}/{2}'.format(b, e, d)
        else:
            raise NotImplementedError('Backends other that "sqlite" are not supported.')

    def __getitem__(self, k):
        return getattr(self, k)

    def __setitem__(self, k, v):
        if str(k) in ['save', 'items', 'update']:
            raise NameError('Invalid key ({0})!'.format(k))
        setattr(self, k, v)

    def __init__(self):
        # exa configuration
        self.username = getpass.getuser()
        self.interactive = False if hasattr(_m, '__file__') else True
        self.system = platform.system().lower()
        self.developer = False
        self.maxlogsize = 10 * 1024 * 1024
        if self.system == 'windows':
            self.home = os.getenv('USERPROFILE')
        else:
            self.home = os.getenv('HOME')
        # exa directories and logs
        self.exa = mkpath(self.home, '.exa_new', mkdir=True)    # TODO: replace with original .exa
        self.keys = mkpath(self.exa, 'keys', mkdir=True)
        self.containers = mkpath(self.exa, 'containers', mkdir=True)
        self.auxiliary = mkpath(self.exa, 'auxiliary', mkdir=True)
        self.syslog = mkpath(self.exa, 'system.log')
        self.unitlog = mkpath(self.exa, 'unittest.log')
        self.doclog = mkpath(self.exa, 'doctest.log')
        self.rellog = mkpath(self.exa, 'relational.log')
        self.numlog = mkpath(self.exa, 'numerical.log')
        self.userlog = mkpath(self.exa, 'user.log')
        self.jslog = mkpath(self.exa, 'js.log')
        # Packages' paths
        self.pkg = os.path.dirname(__file__)
        self.templates = mkpath(self.pkg, 'templates')
        self.static = mkpath(self.pkg, 'static')
        self.img = mkpath(self.static, 'img')
        self.css = mkpath(self.static, 'css')
        self.js = mkpath(self.static, 'js')
        self.extensions = mkpath(jupyter_data_dir(), 'nbextensions', 'exa_new')
        # Databases
        self.relational = {'backend': 'sqlite', 'host': None,
                           'database': 'exa.sqlite', 'user': None}
        self.numerical = {'backend': 'hdf5', 'host': None,
                          'database': None, 'user': None}
        # Update existing
        existing_config = mkpath(self.exa, 'config.yml')
        if os.path.isfile(existing_config):
            with open(existing_config) as f:
                self.update(yaml.load(f))

    def __repr__(self):
        return yaml.dump(self.__dict__, default_flow_style=False)


# Initialize the configuration
Config = Config()


# API cleanup
del _m, getpass, platform, jupyter_data_dir
