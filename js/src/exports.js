// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Exported Modules
 */
"use strict";
var _ = require("underscore");


module.exports = _.extend({}, {
        version: require("../package.json").version
    },
    require("./base.js"),
    require("./apibuilder.js")
);
