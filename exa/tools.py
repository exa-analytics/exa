'''
Tools
====================
Require internal (exa) imports.
'''
import shutil, os
from notebook import install_nbextension
from exa import Config, re
from exa.utils import mkpath


def install_widget_javascript(path=None, verbose=False):
    '''
    '''
    try:
        shutil.rmtree(Config.extensions)
    except:
        pass
    for root, subdirs, files in os.walk(Config.js):
        for filename in files:
            original_filepath = mkpath(root, filename)
            sstr = '^(.*static.js)'
            rmprefix = re.search(sstr, original_filepath)
            dest = Config.extensions
            dest += original_filepath.replace(rmprefix.group(1), '').replace(filename, '')
            mkpath(dest, mkdir=True)
            install_nbextension(original_filepath, verbose=verbose,
                                overwrite=True, nbextensions_dir=dest)
