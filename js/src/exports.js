// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Exported Modules
 */
"use strict";
var _ = require("underscore");


module.exports = _.extend({},
    require("./base.js"),
    require("./tests/test_base.js"),
    require("./imports.js"),
    require("./apibuilder.js")
);
module.exports['version'] = require("../package.json").version;
