// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*""""
Tests for exa-abcwidgets
========================================
*/
"use strict";
var QUnit = require("qunitjs");
console.log(QUnit);


class TestABCWidgets {
    constructor(ignored=["constructor"]) {
        if (ignored.includes("constructor")) {
        } else {
            ignored.push("constructor");
        }
        this.ignored = ignored;
        console.log(this.ignored);
        this.runner()
    }

    runner() {
        for (var method in Object.getOwnPropertyNames(this)) {
            console.log(method);
            if (this.ignored.includes(method)) {
            } else {
                this.call(method, this);
            }
        }
    }
}


module.exports = {
    "TestABCwidgets": TestABCWidgets
}
