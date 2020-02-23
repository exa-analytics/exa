#!/usr/bin/env bash
# Execute from the repo's root directory
rm -rf docs/source/*.txt
SPHINX_APIDOC_OPTIONS=members,undoc-members,show-inheritance sphinx-apidoc -eM -s txt -o docs/source/ exa *test*
cd docs
make html
