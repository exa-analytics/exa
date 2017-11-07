#!/usr/bin/env python
from glob import glob
from subprocess import check_call


def compile_js():
    for path in glob("src/*.ts"):
        print(path)
        check_call(["tsc", path])
    check_call("npm install")


if __name__ == "__main__":
    compile_js()
