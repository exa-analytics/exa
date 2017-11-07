// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/**
 * Automatic Python API generation for JavaScript libraries.
 *
 * This module scans predefined third party JavaScript libraries (e.g. three.js)
 * and identifies top level objects for which an API is dynamically generated.
 * This API allows developers and users to access features of third-party
 * libraries directly from Python (through the ipywidgets - itself built on
 * Backbone.js - infrastructure). An attempt is made to provide a fully featured
 * API automatically but this may not always be possible.
 *
 * See the style comment in base.js for technical information about syntax and
 * style.
 */
function onmessage(e) {
    console.log("onmessage");
    build(e.mod);
}

function build_mv(name, obj) {
    console.log("building: " + name);
}


export function build(mod) {
    console.log("In build...");
    console.log(mod);
    for (var name of Object.getOwnPropertyNames(mod)) {
        console.log("getting obj");
        var obj = mod[name];
        console.log(obj);
        var mv = build_mv(name, obj);
        break
    };
}


