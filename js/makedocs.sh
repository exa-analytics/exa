if [ -f node_modules/win.txt ]; then
    rm -rf node_modules
fi
npm install jsdoc
npm install jsdoc-sphinx
touch node_modules/nix.txt
rm -rf ../docs/source/js
./node_modules/.bin/jsdoc -t node_modules/jsdoc-sphinx/template/ -d ../docs/source/js/ -r src/
rm -rf ../docs/source/js/conf.py
