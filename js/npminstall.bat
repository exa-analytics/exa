CALL del /q /s /q node_modules/jsdoc_sphinx 1>nul
CALL rmdir /s /q node_modules/jsdoc_sphinx
CALL npm install
CALL jupyter nbextension install exa --py --sys-prefix --overwrite
CALL jupyter nbextension enable exa --py --sys-prefix
