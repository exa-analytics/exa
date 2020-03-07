# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Static Data Directory
#############################################
Provide the location of the static data.
"""
import exa


def staticdir():
    exa.cfg.log.warning("use of exa.static is deprecated. use exa.cfg")
    return exa.cfg.staticdir


def resource(name):
    exa.cfg.log.warning("use of exa.static is deprecated. use exa.cfg")
    return exa.cfg.resource(name)
