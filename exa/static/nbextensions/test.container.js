/*"""
===================================
container.test.js
===================================
A test application called when an empty container widget is rendered in a
Jupyter notebook environment.
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/tester': {
            exports: 'Tester'
        },
    },
});


define(['nbextensions/exa/tester'], function(Tester) {
    class TestContainer extends Tester {
        /*"""
        TestContainer
        ==============
        A test application for the container
        */
        constructor() {
            super();
            console.log(this.obj);
        }
    };

    return TestContainer;
});
