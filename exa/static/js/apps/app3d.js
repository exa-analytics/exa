/*"""
===============
app3d.js
===============
A 3D visualization application utilizing the three.js library. This application
is responsible for creating a Three.js scene on an HTML canvas with some
reasonable default options (for camera, lighting, etc.) that can either be
extended (subclasses) or modified after instance createion.
*/
'use strict';


require.config({
    shim: {
        '../adapters/threejs': {
            exports: 'adapt3js'
        },
    },
});


define(['../adapters/threejs'], function(adapt3js) {
    class App3D {
        /*"""
        App3D
        =========
        A 3D visualization application built on top of threejs
        */
        constructor(canvas) {
            this.threejs_adapter = new adapt3js.ThreeJSAdapter(canvas);
        }

    };

    return {App3D: App3D};
});
