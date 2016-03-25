/*"""
===============
three.app.js
===============
This module provides wrappers around the `three.js`_ API for creating objects
and scenes (using the WebGL renderer). The purpose of these wrappers is to
standardize the interface to three.js when input data (such as x, y, z
coordinates) always comes from dataframe (or dataframe-like) structures. Data-
specific packages (e.g. `atomic`_) can either use the functionality provided
here or futher adapt it to suit their needs.

.. _three.js: http://threejs.org/
.. _atomic: https://github.com/exa-analytics/atomic
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

        'nbextensions/exa/marchingcubes': {
            exports: 'MarchingCubes'
        },

        'nbextensions/exa/utility': {
            exports: 'utility'
        },
    },
});


define([
    'nbextensions/exa/lib/three.min',
    'nbextensions/exa/lib/TrackballControls',
    'nbextensions/exa/marchingcubes',
    'nbextensions/exa/utility'
], function(
    THREE,
    TrackballControls,
    MarchingCubes,
    utility
) {
    var ThreeJSApp = function(canvas) {
        /*"""
        ThreeJSApp
        ==============
        A wrapper class (around the three.js functionality) used for transcribing
        Python trait data into renderable data.
        */
        this.canvas = canvas;
        this.width = this.canvas.width();
        this.height = this.canvas.height();

        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas.get(0),
            antialias: true,
        });
        this.renderer.setClearColor(0xFFFFFF);
        this.renderer.setPixelRatio( window.devicePixelRatio );
        this.renderer.setSize(this.width, this.height);

        this.scene = new THREE.Scene();

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
        this.controls.addEventListener('change', this.render.bind(this));

        this.dlight1 = new THREE.DirectionalLight(0xFFFFFF, 0.4);
        this.dlight1.position.set(0, 100, 100);
        this.scene.add(this.dlight1);
        this.dlight2 = new THREE.DirectionalLight(0xFFFFFF, 0.4);
        this.dlight2.position.set(100, 0, 100);
        this.scene.add(this.dlight2);
        this.ambient_light = new THREE.AmbientLight(0xFFFFFF);
        this.scene.add(this.ambient_light);
    };

    ThreeJSApp.prototype.render = function() {
        /*"""
        render
        -----------
        Render the 3D application
        */
        this.renderer.render(this.scene, this.camera);
    };

    ThreeJSApp.prototype.animate = function() {
        /*"""
        animate
        ------------
        Start the animation.
        */
        window.requestAnimationFrame(this.animate.bind(this));
        this.controls.update();
    };

    ThreeJSApp.prototype.resize = function() {
        /*"""
        resize
        ------------
        Resizing of the renderer and controls
        */
        this.width = this.canvas.width();
        this.height = this.canvas.height();
        this.renderer.setSize(this.width, this.height);
        this.camera.aspect = this.width / this.height;
        this.camera.updateProjectionMatrix();
        this.controls.handleResize();
        this.render();
    };

    ThreeJSApp.prototype.add_spheres = function(positions, colors, radii, material) {
        /*"""
        add_sphere
        -------------
        Add's SphereBufferGeometry objects from the given positions with the
        given radii, colors, and material.

        If no colors or radii (or material) are provided, suitable defaults will
        chosen.

        Args:
            positions (object): An N x 3 array like object
            colors (object): List like colors corresponding to every object
            radii (object): List like radii corresponding to every object
            material (THREE.Material): Three.js material object

        Warning:
            On a modern machine attempting to render >50k (approximately) objects
            will cause a slowdown of the browser and framerate of the render
            down to barely usable speeds.

        See Also:
            **add_points**
        */
        colors = colors || [0x808080];
        radii = radii || [1.0];
        material = material || THREE.MeshLambertMaterial;
        var unique_radii = utility.unique(radii);
        var unique_colors = utility.unique(colors);
        var nunique = unique_radii.length;
        var geometries = [];
        var materials = [];
        for (var i=0; i<nunique; i++) {
            geometries.push(new THREE.SphereBufferGeometry(unique_radii[i]));
            materials.push(new material({
                color: unique_colors[i],
            }));
        };
        if (typeof positions[0] == 'object') {
            var n = positions.length;
            for (let i=0; i<n; i++) {
                var color;
                var radius;
                if (nunique == 1) {
                    color = colors[0];
                    radius = radii[0];
                } else {
                    color = colors[i];
                    radius = radii[i];
                };
                var index = unique_colors.indexOf(color);
                var mesh = new THREE.Mesh(geometries[index], materials[index]);
                mesh.position.set(positions[i][0], positions[i][1], positions[i][2]);
                this.scene.add(mesh);
            };
        } else {
            console.log('not implemented');
        };
    };

    ThreeJSApp.prototype.add_points = function(x, y, z, colors, radii) {
        /*"""
        add_points
        ---------------
        Create a point cloud from positions, colors, and radii.

        Args:
            x (array-like): Array like object of x values
            y (array-like): Array like object of y values
            z (array-like): Array like object of z values
            colors (object): List like colors corresponding to every object
            radii (object): List like radii corresponding to every object

        Warning:
            On a modern machine attempting to render >5 million (approximately)
            objects can cause a slowdown of the browser and framerate of the
            application.
        */
        colors = colors || 1;
        radii = radii || 1;
        var geometry = new THREE.BufferGeometry();
        var material = new THREE.ShaderMaterial({
            vertexShader: this.vertex_shader,
            fog: true,
            fragmentShader: this.point_frag_shader,
            transparent: true,
            opacity: 0.8
        });
        console.log(x);
        console.log(y);
        console.log(z);
        var xyz = utility.create_float_array_xyz(x, y, z);
        var n = Math.floor(xyz.length / 3);
        if (!colors.hasOwnProperty('length')) {
            colors = utility.repeat_object(0x808080, n);
        };
        if (!radii.hasOwnProperty('length')) {
            radii = utility.repeat_float(1.0, n);
        };
        colors = this.flatten_color(colors);
        radii = new Float32Array(radii);
        geometry.addAttribute('position', new THREE.BufferAttribute(xyz, 3));
        geometry.addAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.addAttribute('size', new THREE.BufferAttribute(radii, 1));
        var points = new THREE.Points(geometry, material);
        this.scene.add(points);
    };

    ThreeJSApp.prototype.flatten_color = function(colors) {
        /*"""
        flatten_color
        ------------------
        */
        var n = colors.length;
        console.log(n);
        console.log(colors);
        var flat = new Float32Array(n * 3);
        for (let i=0, i3=0; i<n; i++, i3+=3) {
            var color = new THREE.Color(colors[i]);
            flat[i3] = color.r;
            flat[i3+1] = color.g;
            flat[i3+2] = color.b;
        };
        console.log(flat);
        return flat;
    };

    ThreeJSApp.prototype.add_lines = function() {
        /*"""
        add_lines
        ------------
        */
    };

    ThreeJSApp.prototype.test_mesh = function() {
        /*"""
        test_mesh
        ---------------
        Example of a render
        */
        this.test_geometry = new THREE.BoxGeometry(2.0, 2.0, 2.0);
        this.test_material = new THREE.MeshLambertMaterial({color: 0x005500});
        this.test_cube = new THREE.Mesh(this.test_geometry, this.test_material);
        this.scene.add(this.test_cube);
        this.camera.position.x = 100;
        this.camera.position.y = 100;
        this.camera.position.z = 100;
        this.target = new THREE.Vector3(0, 0, 0);
        this.camera.lookAt(this.target);
        this.controls.target = this.target;
    };

    ThreeJSApp.prototype.default_camera = function(x, y, z, ox, oy, oz) {
        /*"""
        default_camera
        ------------------
        Set the camera in the default position and have it look at the origin.

        Args:
            x (float): Camera position in x
            y (float): Camera position in y
            z (float): Camera position in z
            ox (float): Target position in x
            oy (float): Target position in y
            oz (float): Target position in z
        */
        x = x || 100;
        y = y || 100;
        z = z || 100;
        ox = ox || 0;
        oy = oy || 0;
        oz = oz || 0;
        this.camera.position.set(x, y, z);
        this.target = new THREE.Vector3(ox, oy, oz);
        this.camera.lookAt(this.target);
        this.controls.target = this.target;
    };

    // These are shaders written in GLSL (GLslang: OpenGL Shading Language).
    // This code is executed on the GPU.
    ThreeJSApp.prototype.vertex_shader = "\
        attribute float size;\
        attribute vec3 color;\
        varying vec3 vColor;\
        \
        void main() {\
            vColor = color;\
            vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);\
            gl_PointSize = size * (600.0 / length(mvPosition.xyz));\
            gl_Position = projectionMatrix * mvPosition;\
        }\
    ";

    ThreeJSApp.prototype.point_frag_shader = "\
        varying vec3 vColor;\
        \
        void main() {\
            if (length(gl_PointCoord * 2.0 - 1.0) > 1.0)\
                discard;\
            gl_FragColor = vec4(vColor, 1.0);\
        }\
    ";

    ThreeJSApp.prototype.circle_frag_shader = "\
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

    ThreeJSApp.prototype.line_frag_shader = "\
        uniform vec3 color;\
        uniform float opacity;\
        \
        vary vec3 vColor;\
        void main() {\
            gl_FragColor = vec4(vColor * color, opacity);\
        }\
    ";

    ThreeJSApp.prototype.line_vertex_shader = "\
        uniform float amplitude;\
        attribute vec3 displacement;\
        attribute vec3 customColor;\
        varying vec3 vColor;\
        \
        void main() {\
            vec3 newPosition = position + amplitude * displacement;\
            vColor = customColor;\
            gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);\
        }\
    ";

    return {'ThreeJSApp': ThreeJSApp};
});
