#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Launcher
#############
"""
import argparse
from exa.app import ExaApp, ExaNotebook


def main():
    parser = argparse.ArgumentParser(description="The exa framework launcher.")
    parser.add_argument(
        "-nb",
        "--notebook",
        action="store_true",
        help="Starts a Jupyter notebook server in the exa notebook directory.",
        required=False,
        default=False
    )
    args = parser.parse_args()
    print(args)
    if args.notebook:
        ExaNotebook.launch_instance()
    else:
        ExaApp.launch_instance()


if __name__ == "__main__":
    main()
