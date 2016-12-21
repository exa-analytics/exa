#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Launchers
#############
This module provides all front-facing command line actions. By default running
exa starts exa's Jupyter notebook interface.
"""
import argparse
from exa.app import ExaApp, ExaNotebook


def main():
    parser = argparse.ArgumentParser(description="The exa framework launcher.")
    #args = parser.parse_args()
    ExaNotebook.launch_instance()


if __name__ == "__main__":
    main()
