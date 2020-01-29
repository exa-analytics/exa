# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
#import six as _six
import os as _os
import sys as _sys
import bz2 as _bz2
from pandas import read_json as _rj
from exa import Editor as _E
from exa import DataFrame as _DF
if not hasattr(_bz2, "open"):
    _bz2.open = _bz2.BZ2File




def _create():
    """Globally called function for creating the isotope/element API."""

def as_df():
    """Return a dataframe of isotopes."""
    records = []
    for sym, ele in vars(_this).items():
        if sym not in ["Element", "Isotope"] and not sym.startswith("_"):
            for k, v in vars(ele).items():
                if k.startswith("_") and k[1].isdigit():
                    records.append({kk: vv for kk, vv in vars(v).items() if not kk.startswith("_")})
    return _DF.from_records(records)


# Data order of isotopic (nuclear) properties:
_resource = "../../static/isotopes.json"    # HARDCODED
_columns = ("A", "Z", "af", "afu", "cov_radius", "van_radius", "g", "mass", "massu", "name",
            "eneg", "quad", "spin", "symbol", "color")
_this = _sys.modules[__name__]         # Reference to this module
_path = _os.path.abspath(_os.path.join(_os.path.abspath(__file__), _resource))
if not hasattr(_this, "H"):
    _create()
