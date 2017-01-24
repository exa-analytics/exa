#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
App Launcher
##############
Launches a `Jupyter notebook`_ in Exa's root directory.
"""
import argparse
from exa.app import Notebook


def main():
    """Main application launcher."""
    parser = argparse.ArgumentParser(description="Exa notebook app launcher.")
    args = parser.parse_args()
    Notebook.launch_instance()


if __name__ == "__main__":
    main()
