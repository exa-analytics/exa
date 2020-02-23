# Execute from the repo's root directory
del /f docs\source\*.txt
set SPHINX_APIDOC_OPTIONS=members,undoc-members,show-inheritance
sphinx-apidoc -eM -s txt -o docs\source\ exa *test*
cd docs
make.bat html
