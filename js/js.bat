REM Helper script for development on windows
call npm install
call jupyter nbextension install --py --sys-prefix exa
call jupyter nbextension enable --py --sys-prefix exa
