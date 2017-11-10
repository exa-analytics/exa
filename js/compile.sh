#!/usr/bin/env bash
# Compile and install the web extension package.

for path in `ls src/*.ts`; do
    echo -e "\nCompiling TypeScript: $path";
    tsc $path;
done

echo -e "\nInstalling JavaScript"
npm install
