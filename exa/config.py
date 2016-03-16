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


class Config:
    '''
    The Config class is essentially a dictionary of parameters.
    See the documentation in the module's docstring.
    '''

    def save(self):
        try:
            confpath = os.sep.join((self.exa, 'config.json'))
            with open(confpath, 'w') as f:
                json.dump(vars(self), f)
        except:
            pass

    def update(self, other=None):
        if hasattr(other, 'items'):
            for k, v in other.items():
                if v and k != 'ipynb':
                    self[k] = v

    def cleanup(self):
        try:
            shutil.rmtree(self.exa)
        except:
            pass

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
        self.exa = os.sep.join((self.home, '.exa'))    # Dir config
        if os.path.isdir(self.exa):
            self._temp = False
        else:
            self.exa = os.sep.join((gettempdir(), 'exa'))
            os.makedirs(self.exa, exist_ok=True)
            self._temp = True
        interactive = True
        try:
            cfg = get_ipython().config
            if 'IPKernelApp' in cfg:
                interactive = True
            else:
                interactive = False
        except:
            interactive = False
        self.interactive = interactive
        self.syslog = os.sep.join((self.exa, 'system.log'))        # Backend log
        self.testlog = os.sep.join((self.exa, 'test.log'))         # Unit and doc tests
        self.userlog = os.sep.join((self.exa, 'user.log'))         # Frontend log
        self.tmp = os.sep.join((self.exa, 'tmp'))
        os.makedirs(self.tmp, exist_ok=True)
        self.pkg = os.path.dirname(__file__)
        self.templates = os.sep.join((self.pkg, 'templates'))
        self.static = os.sep.join((self.pkg, 'static'))
        self.img = os.sep.join((self.static, 'img'))
        self.css = os.sep.join((self.static, 'css'))
        self.js = os.sep.join((self.static, 'js'))
        self.nbext = os.sep.join((self.static, 'nbextensions'))
        self.extensions = os.sep.join((jupyter_data_dir(), 'nbextensions', 'exa'))
        os.makedirs(self.extensions, exist_ok=True)
        self.relational = {'backend': 'sqlite', 'host': None,
                           'database': None, 'user': None}
        self.numerical = {'backend': None, 'host': None,
                          'database': None, 'user': None}
        existing_config = os.sep.join((self.exa, 'config.json'))   # Update existing
        if os.path.isfile(existing_config):
            with open(existing_config) as f:
                self.update(json.load(f))

    def __repr__(self):
        return json.dumps(vars(self), sort_keys=True, indent=4)


Config = Config()    # Config is a singleton to ensure correct scope
