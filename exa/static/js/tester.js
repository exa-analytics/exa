/*"""
===================================
tester.js
===================================
A base JavaScript tester class.
*/
'use strict';


require.config({
    shim: {},
});


define([], function() {
    class Tester {
        /*"""
        Tester
        ============
        Base class for testing applications
        */
        constructor() {
            this.obj = 42;
        };
    };

    return Tester;
});
