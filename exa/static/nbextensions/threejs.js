/*"""
Three.js Adapter
````````````````````````````````
An adapter for the power three.js library.
*/

'use strict';


require.config({
    shim: {
        'nbextensions/exa/lib/three.min': {
            exports: 'THREE'
        },

        'nbextensions/exa/lib/TrackballControls': {
            deps: ['nbextensions/exa/lib/three.min'],
            exports: 'THREE.TrackballControls'
        },

        'nbextensions/exa/lib/marchingcubes': {
            exports: 'MarchingCubes'
        },
    }
});


define([
    'nbextensions/exa/lib/three.min',
    'nbextensions/exa/lib/TrackballControls',
    'nbextensions/exa/lib/marchingcubes'
], function(
    THREE,
    TrackballControls,
    MarchingCubes
) {
    var ThreeJS = function(canvas) {
        this.canvas = canvas;
        console.log(this.canvas);
    };

    ThreeJS.prototype.vertex_shader = "\
        attribute float size;\
        attribute vec3 color;\
        varying vec3 vColor;\
        \
        void main() {\
            vColor = color;\
            vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);\
            gl_PointSize = size * (450.0 / length(mvPosition.xyz));\
            gl_Position = projectionMatrix * mvPosition;\
        }\
    ";

    ThreeJS.prototype.point_frag_shader = "\
        varying vec3 vColor;\
        \
        void main() {\
            if (length(gl_PointCoord * 2.0 - 1.0) > 1.0)\
                discard;\
            gl_FragColor = vec4(vColor, 1.0);\
        }\
    ";

    ThreeJS.prototype.circle_frag_shader = "\
        varying vec3 vColor;\
        \
        void main() {\
            if (length(gl_PointCoord * 2.0 - 1.0) > 1.0)\
                discard;\
            if (length(gl_PointCoord * 2.0 - 1.0) < 0.9)\
                discard;\
            gl_FragColor = vec4(vColor, 1.0);\
        }\
    ";

    return {'ThreeJS': ThreeJS};
});


    /*var ThreeJS = {
        /*"""
        ThreeJS
        -------------
        Custom ThreeJS class.
        init: function(canvas) {
            this.canvas = canvas;
            this.width = this.canvas.width();
            this.height = this.canvas.height();
            this.renderer = new THREE.WebGLRenderer({
                canvas: this.canvas.get(0),
                antialias: true,
            });
            this.renderer.setClearColor(0xFFFFFF);
            this.renderer.setSize(this.width, this.height);
            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(60, this.width / this.height, 0.000001, 100000);
            this.controls = new TrackballControls(this.camera, this.canvas.get(0));
            this.controls.rotateSpeed = 10.0;
            this.controls.zoomSpeed = 5.0;
            this.controls.panSpeed = 0.5;
            this.controls.noZoom = false;
            this.controls.noPan = false;
            this.controls.staticMoving = true;
            this.controls.dynamicDampingFactor = 0.3;
            this.controls.keys = [65, 83, 68];
            this.controls.addEventListener('change', this.render.bind(this));
        },*/
