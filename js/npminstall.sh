#rm -rf node_modules/jsdoc_sphinx
npm install
jupyter nbextension install exa --py --sys-prefix --overwrite
jupyter nbextension enable exa --py --sys-prefix
