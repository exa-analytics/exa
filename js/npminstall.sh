if [ -f node_modules/win.txt ]; then
    rm -rf node_modules dist
fi
npm install
touch node_modules/nix.txt
jupyter nbextension install exa --py --sys-prefix --overwrite
jupyter nbextension enable exa --py --sys-prefix
