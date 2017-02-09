REM Helper to build reStructuredText (RST) files using jsdoc
REM Run from the js\ directory
call npm install
call node_modules\.bin\jsdoc -t .\node_modules\jsdoc-rst-template\template\ -d ..\docs\source\js\jsdoc_rst\ -r src\
call rm ..\docs\source\js\jsdoc_rst\api.rst ..\docs\source\js\jsdoc_rst\index.rst
