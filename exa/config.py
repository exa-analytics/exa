# -*- coding: utf-8 -*-
'''
Configuration
====================================
Stores exa's working configuration.

Attributes:
    username (str): Username (OS level)
    system (str): 'windows', 'linux', 'darwin'
    home (str): User's exa "home" directory (e.g. ~/)
    exa (str): The ".exa" directory (e.g. ~/.exa)
    static (str): Static frontend data directory
    extensions (str): Jupyter's extensions directory
    templates (str): HTML templates directory
    css (str): Static CSS directory
    js (str): Static JavaScript directory
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
import json
from notebook.nbextensions import jupyter_data_dir
from exa.utils import mkpath


class Config:
    '''
    The Config class is essentially a dictionary of parameters.
    See the documentation in the module's docstring.
    '''

    def save(self):
        confpath = mkpath(self.exa, 'config.json')
        with open(confpath, 'w') as f:
            json.dump(vars(self), f)

    def update(self, other=None):
        if hasattr(other, 'items'):
            for k, v in other.items():
                if v:                  # Updates if the value evaluates to True
                    self[k] = v

    def relational_engine(self):
        b = self.relational.backend
        e = self.exa
        d = self.relational.database
        h = self.relational.host
        u = self.relational.user
        if b == 'sqlite':
            return '{0}:///{1}/{2}'.format(b, e, d)
        else:
            raise NotImplementedError('Backends other that "sqlite" are not supported yet.')

    def __getitem__(self, k):
        return getattr(self, k)

    def __setitem__(self, k, v):
        if str(k) in ['save', 'items', 'update']:
            raise NameError('Invalid key ({0})!'.format(k))
        setattr(self, k, v)

    def __init__(self):
        self.username = getpass.getuser()                  # Basic config
        self.system = platform.system().lower()
        self.maxlogbytes = 10 #1024 * 1024
        self.maxlogcount = 5
        if self.system == 'windows':
            self.home = os.getenv('USERPROFILE')
        else:
            self.home = os.getenv('HOME')
        self.exa = mkpath(self.home, '.exa', mkdir=True)    # Dir config
        self.syslog = mkpath(self.exa, 'system.log')        # Backend log
        self.testlog = mkpath(self.exa, 'test.log')         # Unit and doc tests
        self.userlog = mkpath(self.exa, 'user.log')         # Frontend log
        self.pkg = os.path.dirname(__file__)
        self.templates = mkpath(self.pkg, 'templates')
        self.static = mkpath(self.pkg, 'static')
        self.img = mkpath(self.static, 'img')
        self.css = mkpath(self.static, 'css')
        self.js = mkpath(self.static, 'js')
        self.extensions = mkpath(jupyter_data_dir(), 'nbextensions', 'exa')
        self.relational = {'backend': 'sqlite', 'host': None,
                           'database': 'exa.sqlite', 'user': None}
        self.numerical = {'backend': 'hdf5', 'host': None,
                          'database': None, 'user': None}
        existing_config = mkpath(self.exa, 'config.json')   # Update existing
        if os.path.isfile(existing_config):
            with open(existing_config) as f:
                self.update(json.load(f))

    def __repr__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4)


# There is only one configuration object per exa instance
Config = Config()
