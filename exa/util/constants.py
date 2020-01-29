# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
import sys as _sys
import json as _json
from exa import Editor as _Editor
from exa import DataFrame as _DF
from exa.static import resource as _resource


def _create():
    for kwargs in _json.load(_Editor(_path).to_stream()):
        setattr(_this, kwargs['name'], Constant(**kwargs))

def as_df():
    """Return a dataframe of constants."""
    records = []
    for con, attrs in vars(_this).items():
        if con not in ['Constant', 'as_df'] and not con.startswith('_'):
            records.append({k: v for k, v in vars(attrs).items()
                            if not k.startswith('_') and vars(attrs)})
    return _DF.from_records(records)

_this = _sys.modules[__name__]
_path = _resource("constants.json")
if not hasattr(_this, "Planck_constant"):
    _create()
