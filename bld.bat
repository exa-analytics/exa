"%PYTHON%" setup.py install
jupyter nbextension install exa --py --sys-prefix --overwrite
jupyter nbextension enable exa --py --sys-prefix
if errorlevel 1 exit 1
