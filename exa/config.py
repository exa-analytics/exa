# -*- coding: utf-8 -*-
'''
Configuration
====================================
Stores exa's working configuration.

Note:
    The Configuration class is called "Config" and is not visible in the
    documentation because it is a singleton: the class object instance is
    set to an instance of itself.
'''
import os
import getpass
import platform
import json
import shutil
from tempfile import gettempdir
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
                if v and k != 'ipynb':
                    self[k] = v

    def cleanup(self):
        shutil.rmtree(self.exa)

    def relational_engine(self):
        b = self.relational['backend']
        e = self.exa
        d = self.relational['database']
        h = self.relational['host']
        u = self.relational['user']
        if b == 'sqlite':
            if h is None:
                return '{0}://'.format(b)
            else:
                return '{0}:///{1}/{2}'.format(b, e, d)
        else:
            raise NotImplementedError('Backends other that "sqlite" are not supported yet.')

    def session_args(self):
        '''
        Generate kwargs to load a session.

        See Also:
            :func:`~exa.relational.Dashboard.load`
        '''
        return (self.session, self.program, self.project, self.job, self.container)

    def __getitem__(self, k):
        return getattr(self, k)

    def __setitem__(self, k, v):
        if str(k) in ['save', 'items', 'update']:
            raise NameError('Invalid key ({0})!'.format(k))
        setattr(self, k, v)

    def __init__(self):
        self.username = getpass.getuser()                  # Basic config
        self.ipynb = False
        kernel = None                                      # Check if using
        try:                                               # Jupyter notebook
            kernel = get_ipython().kernel
            self.ipynb = True
        except:
            pass
        self.numba = False
        try:
            import numba                                   # Check if numba is
            self.numba = True                              # available
        except:
            pass
        self.system = platform.system().lower()
        self.max_log_bytes = 10 * 1024 * 1024
        self.max_log_count = 5
        self.max_anon_sessions = 5
        self.gc = 500                                      # Custom garbage collection
        self.session = None
        self.program = None
        self.project = None
        self.job = None
        self.container = None
        if self.system == 'windows':
            self.home = os.getenv('USERPROFILE')
        else:
            self.home = os.getenv('HOME')
        self.exa = mkpath(self.home, '.exa')    # Dir config
        if os.path.isdir(self.exa):
            self._temp = False
        else:
            self.exa = mkpath(gettempdir(), 'exa', mkdir=True)
            self._temp = True
        self.syslog = mkpath(self.exa, 'system.log')        # Backend log
        self.testlog = mkpath(self.exa, 'test.log')         # Unit and doc tests
        self.userlog = mkpath(self.exa, 'user.log')         # Frontend log
        self.tmp = mkpath(self.exa, 'tmp')
        self.pkg = os.path.dirname(__file__)
        self.templates = mkpath(self.pkg, 'templates')
        self.static = mkpath(self.pkg, 'static')
        self.img = mkpath(self.static, 'img')
        self.css = mkpath(self.static, 'css')
        self.js = mkpath(self.static, 'js')
        self.nbext = mkpath(self.static, 'nbextensions')
        self.extensions = mkpath(jupyter_data_dir(), 'nbextensions', 'exa')
        self.relational = {'backend': 'sqlite', 'host': None,
                           'database': None, 'user': None}
        self.numerical = {'backend': None, 'host': None,
                          'database': None, 'user': None}
        existing_config = mkpath(self.exa, 'config.json')   # Update existing
        if os.path.isfile(existing_config):
            with open(existing_config) as f:
                self.update(json.load(f))

    def __repr__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4)


Config = Config()    # Config is a singleton to ensure correct scope
