IF EXIST node_modules\nix.txt rd /s /q node_modules dist 
CALL npm install
CALL type nul > node_modules\win.txt 
CALL jupyter nbextension install exa --py --sys-prefix --overwrite
CALL jupyter nbextension enable exa --py --sys-prefix
