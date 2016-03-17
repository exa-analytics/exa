# -*- coding: utf-8 -*-
from exa import _conf

if _conf['pkg_numba']:
    from exa.algorithms.jitted import vmag3, vdist3
else:
    from exa.algorithms.broadcasting import vmag3, vdist3
