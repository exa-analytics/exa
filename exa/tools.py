'''
Tools
====================
Require internal (exa) imports.
'''
import shutil, os
from notebook import install_nbextension
from exa import Config
from exa import _re as re
from exa.utils import mkpath


def install_notebook_widgets(path=None, verbose=False):
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
            install_nbextension(
                original_filepath,
                verbose=verbose,
                overwrite=True,
                nbextensions_dir=dest
            )


def initialize_database():
    pass

    #for tbl in Dimension.__subclasses__() + [Isotope, Constant]:
#    count = 0
#    try:
#        count = DB[tbl.__tablename__].count()
#    except:
#        pass
#    if count == 0:
#        print('Loading {0} data'.format(tbl.__tablename__))
#        data = None
#        if tbl.__tablename__ == 'isotopes':
#            with open(mkpath(Config.static, 'isotopes.yml')) as f:
#                data = yaml.load(f, Loader=Loader)
#            data = list(data.values())
#        elif tbl.__tablename__ == 'constants':
#            with open(mkpath(Config.static, 'constants.yml')) as f:
#                data = yaml.load(f, Loader=Loader)['constants']
#            data = list({'symbol': key, 'value': value} for key, value in data.items())
#        else:
#            with open(mkpath(Config.static, 'units.yml')) as f:
#                data = yaml.load(f, Loader=Loader)[tbl.__tablename__]
#            labels = list(data.keys())
#            values = np.array(list(data.values()))
#            cols = list(product(labels, labels))
#            values_t = values.reshape(len(values), 1)
#            l = (values / values_t).ravel()
#            data = [{'from_unit': cols[i][0], 'to_unit': cols[i][1], 'factor': l[i]} for i in range(len(l))]
#        tbl._bulk_save(data)
