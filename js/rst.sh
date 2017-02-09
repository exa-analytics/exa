#!/usr/bin/env bash
# Helper to build reStructuredText (RST) files using jsdoc
# Run from the js/ directory
npm install
./node_modules/.bin/jsdoc -t ./node_modules/jsdoc-rst-template/template/ -d ../docs/source/js/jsdoc_rst/ -r src/
rm ../docs/source/js/jsdoc_rst/api.rst ../docs/source/js/jsdoc_rst/index.rst
