#!/usr/bin/env bash
# Helper to build reStructuredText (RST) files using jsdoc
# Run from the js/ directory
# Run 'npm install' first if necessary
./node_modules/.bin/jsdoc -t node_modules/jsdoc-sphinx/ -d ../docs/source/js/jsdoc_rst/ -r src/
rm ../docs/source/js/jsdoc_rst/index.rst ../docs/source/js/jsdoc_rst/conf.py
