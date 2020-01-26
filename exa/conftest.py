# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Useful pytest fixtures
#######################################
"""

import pytest

import exa


@pytest.fixture(scope='session')
def isotopes():
    iso = exa.Isotopes()
    iso.data()
    return iso
