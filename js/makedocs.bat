REM Helper to build reStructuredText (RST) files using jsdoc
REM Run from the js\ directory
REM Run 'npm install' first if necessary
IF EXIST node_modules\nix.txt rd /s /q node_modules
CALL npm install jsdoc
CALL npm install jsdoc-sphinx
CALL type nul > node_modules\win.txt 
CALL rd /s /q ..\docs\source\js
CALL node_modules\.bin\jsdoc -t node_modules\jsdoc-sphinx\template\ -d ..\docs\source\js\ -r src\
CALL del /s /q ..\docs\source\js\conf.py
