"use strict";
exports.__esModule = true;
// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/* Utilities
 * @desc Utilities for use by the package.
 */
function extend(first, second) {
    var result = {};
    for (var item in first) {
        result[item] = first[item];
    }
    for (var item in second) {
        result[item] = second[item];
    }
    return result;
}
exports.extend = extend;
