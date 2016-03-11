# -*- coding: utf-8 -*-
__exa_version__ = (0, 2, 0)    # Version number is defined here!
__version__ = '.'.join((str(v) for v in __exa_version__))


import atexit as _ae
import seaborn as _sns
_sns.set_context('poster', font_scale=1.3)    # This may override user plotting
_sns.set_palette('colorblind')                # defaults...
_sns.set_style('white')


from exa._config import _conf, show_conf, _cleanup_exa_root
from exa.log import log_names, log_head, log_tail
from exa.test import unit_tests, doc_tests
from exa import tests
from exa import relational


if _conf['exa_persistent']:
    pass    # Eventually do something here
else:
    from exa._install import install
    install()


_ae.register(_cleanup_exa_root)


#_ae.register(Config.save)
#from exa.log import log_tail, log_head, setup
#setup()
#from exa.testing import run_unittests, run_doctests
#from exa.frame import DataFrame
#from exa.relational import Container
#from exa.editor import Editor
#_ae.register(relational.cleanup_sessions)
#_ae.register(relational.commit)
#if Config._temp:
#    _ae.register(Config.cleanup)
#    relational.create_all()
#if Config.interactive:
#    from exa.install import initialize_database
#    initialize_database()
