REM Helper to build reStructuredText (RST) files using jsdoc
REM Run from the js\ directory
REM Run 'npm install' first if necessary
call node_modules\.bin\jsdoc -t .\node_modules\jsdoc-sphinx\template\ -d ..\docs\source\js\jsdoc_rst\  src\exa-abcwidgets.js
call rm ..\docs\source\js\jsdoc_rst\index.rst ..\docs\source\js\jsdoc_rst\conf.py
