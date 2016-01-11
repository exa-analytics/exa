/*"""
Three JS Application (App)
````````````````````````````

*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/static/js/libs/three.min': {
            exports: 'THREE'
        },
        'nbextensions/exa/static/js/libs/TrackballControls': {
            deps: ['nbextensions/exa/static/js/libs/three.min'],
            exports: 'THREE.TrackballControls'
        }
    }
});

define([
    'nbextensions/exa/static/js/libs/three.min',
    'nbextensions/exa/static/js/libs/TrackballControls'
], function(
    THREE,
    TrackballControls
) {
    var threejs = function(width, height, canvas) {
        this.width = width;
        this.height = height;

        this.render = function() {
            this.renderer.render(this.scene, this.camera);
        };

        this.resize = function(width, height) {
            this.width = width - canvas.sidebarwidth;
            this.height = height;
            this.renderer.setSize(this.width, this.height);
            this.camera.aspect = this.width / this.height;
            this.camera.updateProjectionMatrix();
            this.controls.handleResize();
            this.render();
        };

        //this.animate = function() {
        //    window.requestAnimationFrame(this.animate.bind(this));
        //    this.controls.update();
        //};

        // Canvas
        this.canvas = canvas;
        //this.height = this.canvas.height();
        //this.width = this.canvas.width();
        console.log(this.width);
        console.log(this.height);

        // Renderer
        this.renderer = new THREE.WebGLRenderer({
            'canvas': this.canvas.get(0),
            'antialias': true
        });
        this.renderer.setClearColor(0xFFFFFF);
        this.renderer.setSize(this.width, this.height);

        // Scene
        this.scene = new THREE.Scene();
        //var bmat = new THREE.MeshPhongMaterial({
        //    'color': '#003399',
        //    'specular': '#003399',
        //    'transparent': true,
        //    'opacity': 0.5,
        //    'shininess': 15
        //});
        //var omat = new THREE.MeshPhongMaterial({
        //    'color': '#FF9900',
        //    'specular': '#FF9900',
        //    'transparent': true,
        //    'opacity': 0.5,
        //    'shininess': 15
        //});
        //var sph1 = new THREE.SphereGeometry(1.25, 12, 12);
        //var sph2 = new THREE.SphereGeometry(0.75, 12, 12);
        //var mesh1 = new THREE.Mesh(sph1, bmat);
        //var mesh2 = new THREE.Mesh(sph2, omat);
        //mesh1.position.x = 3;
        //mesh1.position.y = 3;
        //mesh1.position.z = 3;
        //mesh2.position.x = -3;
        //mesh2.position.y = -3;
        //mesh2.position.z = -3;
        //this.scene.add(mesh1);
        //this.scene.add(mesh2);
        //console.log(this.scene);

        this.mat = new THREE.LineBasicMaterial({'color': '#FF9900'});
        this.geom = new THREE.BoxGeometry(1, 1, 1);
        this.mesh = new THREE.Mesh(this.geom, this.mat);
        this.scene.add(this.mesh);



        // Camera and controls
        this.camera = new THREE.PerspectiveCamera(60, this.width / this.height, 0.0001, 10000);
        this.controls = new TrackballControls(this.camera, this.canvas.get(0));
        this.controls.rotateSpeed = 10.0;
        this.controls.zoomSpeed = 5.0;
        this.controls.panSpeed = 0.5;
        this.controls.noZoom = false;
        this.controls.noPan = false;
        this.controls.staticMoving = true;
        this.controls.dynamicDampingFactor = 0.3;
        this.controls.keys = [65, 83, 68];
        //this.controls.addEventListener('change', this.render.bind(this));
    };

    //threejs.prototype.render = function() {
    //    this.renderer.render(this.scene, this.camera);
    //};

    return threejs;

});
