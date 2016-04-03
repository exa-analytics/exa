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

        Returns:
            points (THREE.Points): Reference to added points object

        Tip:
            By tracking the returned object, one can create animations.

        Warning:
            On a modern machine attempting to render >5 million (approximately)
            objects can cause a slowdown of the browser and framerate of the
            application.
        */
        if (colors === undefined) {
            colors = 1;
        };
        if (radii == undefined) {
            radii = 1;
        }
        var geometry = new THREE.BufferGeometry();
        var material = new THREE.ShaderMaterial({
            vertexShader: this.vertex_shader,
            fog: true,
            fragmentShader: this.point_frag_shader,
            transparent: true,
            opacity: 1.0
        });
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
        return points;
    };

    ThreeJSApp.prototype.add_lines = function(v0, v1, x, y, z, colors) {
        /*"""
        add_lines
        ------------
        Add lines between pairs of points.

        Args:
            v0 (array): Array of first vertex in pair
            v1 (array): Array of second vertex
            x (array): Position in x of vertices
            y (array): Position in y of vertices
            z (array): Position in z of vertices
            colors (array): Colors of vertices

        Returns:
            linesegs (THREE.LineSegments): Line segment objects
        */
        var material = new THREE.LineBasicMaterial({
            vertexColors: THREE.VertexColors,
            linewidth: 4,
        });
        var geometry = new THREE.Geometry();
        var n = v0.length;
        for (let i=0; i<n; i++) {
            var j = v0[i];
            var k = v1[i];
            var vector0 = new THREE.Vector3(x[j], y[j], z[j]);
            var vector1 = new THREE.Vector3(x[k], y[k], z[k]);
            geometry.vertices.push(vector0);
            geometry.vertices.push(vector1);
            geometry.colors.push(new THREE.Color(colors[j]));
            geometry.colors.push(new THREE.Color(colors[k]));
        };
        var lines = new THREE.LineSegments(geometry, material);
        this.scene.add(lines);
        return lines;
    };

    ThreeJSApp.prototype.flatten_color = function(colors) {
        /*"""
        flatten_color
        ------------------
        */
        var n = colors.length;
        var flat = new Float32Array(n * 3);
        for (let i=0, i3=0; i<n; i++, i3+=3) {
            var color = new THREE.Color(colors[i]);
            flat[i3] = color.r;
            flat[i3+1] = color.g;
            flat[i3+2] = color.b;
        };
        return flat;
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

    ThreeJSApp.prototype.set_camera = function(x, y, z, ox, oy, oz, rx, ry, rz) {
        /*"""
        set_camera
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
        if (x === undefined) {
            x = 100.0;
        };
        if (y === undefined) {
            y = 100.0;
        };
        if (z === undefined) {
            z = 100.0;
        };
        if (ox === undefined) {
            ox = 0.0;
        };
        if (oy === undefined) {
            oy = 0.0;
        };
        if (oz === undefined) {
            oz = 0.0;
        };
        if (rx === undefined) {
            rx = 0.0;
        }
        if (ry === undefined) {
            ry = 0.0;
        }
        if (rz === undefined) {
            rz = 0.0;
        }
        x += rx;
        y += ry;
        z += rz;
        this.camera.position.set(x, y, z);
        this.target = new THREE.Vector3(ox, oy, oz);
        this.camera.lookAt(this.target);
        this.controls.target = this.target;
    };

    ThreeJSApp.prototype.set_camera_from_mesh =  function(mesh, rx, ry, rz) {
        /*"""
        */
        if (rx === undefined) {
            rx = 0.0;
        }
        if (ry === undefined) {
            ry = 0.0;
        }
        if (rz === undefined) {
            rz = 0.0;
        }
        var position;
        if (mesh.geometry.type === 'BufferGeometry') {
            position = mesh.geometry.attributes.position.array;
        } else {
            console.log('NotImplementedError appthreejs323');
        };
        var n = position.length / 3;
        var i = n;
        var oxyz = [0.0, 0.0, 0.0];
        while (i--) {
            oxyz[0] += position[3 * i];
            oxyz[1] += position[3 * i + 1];
            oxyz[2] += position[3 * i + 2];
        };
        oxyz[0] /= n;
        oxyz[1] /= n;
        oxyz[2] /= n;
        mesh.geometry.computeBoundingBox();
        var bbox = mesh.geometry.boundingBox;
        var xyz = bbox.max;
        xyz.x *= 1.2;
        xyz.x += rx;
        xyz.y *= 1.2;
        xyz.y += ry;
        xyz.z *= 1.2;
        xyz.z += rz;
        this.set_camera(xyz.x, xyz.y, xyz.z, oxyz[0], oxyz[1], oxyz[2]);
    };

    ThreeJSApp.prototype.add_single_scalar_field = function(field, isovalue, how) {
        /*"""
        add_single_scalar_field
        -------------------------
        Create an isosurface of a scalar field.

        When given a scalar field, creating a surface requires selecting a set
        of vertices that intersect the provided field magnitude (isovalue).
        There are a couple of algorithms that do this.
        */
        if (how === undefined) {
            how = 'marching cubes single';
        };
        if (how === 'marching cubes single') {
            var mesh0 = this.marching_cubes_single(field, isovalue);
            this.scene.add(mesh0);
            return mesh0
        } else {
            console.log('NotImplementedError');
        };
    };

    ThreeJSApp.prototype.marching_cubes_single = function(field, isovalue) {
        /*"""
        marching_cubes_single
        ------------------------
        Run the marching cubes algorithm finding the volumetric shell that is
        smaller than the isovalue.

        The marching cubes algorithm takes a scalar field and for each field
        vertex looks at the nearest indices (in an evenly space field this
        forms a cube), determines along what edges the scalar field is less
        than the isovalue, and creates new vertices along the edges of the
        field's cube. The at each point in the field, a cube is created with
        vertices numbered:
               4-------5
             / |     / |
            7-------6  |
            |  0----|--1
            | /     | /
            3-------2
        Field values are given for each field vertex. Edges are
        labeled as follows (see the lookup table below).

                                            4
               o-------o                o-------o
             / |     / |            7 / | 6   / |  5
            o-------o  |             o-------o  |
            |  o----|--o             |  o----|--o
          3 | /   0 | / 1            | /     | /
            o-------o                o-------o
               2
        Edges 8, 9, 10, and 11 wrap around (clockwise looking from the top
        as drawn) the vertical edges of the cube, with 8 being the vertical
        edge between vertex 0 and 4 (see above).

        Note:
            Scalar fields are assumed to be in row major order (also known C
            style, and implies that the last index is changing the fastest).

        See Also:
            **field.js**
        */
        console.log('marching cubes single...');
        var nx = field.x.length;
        var ny = field.y.length;
        var nz = field.z.length;
        var nnx = nx - 1;    // Do not use the last vertex of the field data
        var nny = ny - 1;    // when constructing the surface because there is
        var nnz = nz - 1;    // no cube that can be formed for it.
        var cube_vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                   [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]];
        //var cube_vertices = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
        //                     [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]];
        var cube_edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6],
                          [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
        var bits = [1, 2, 4, 8, 16, 32, 64, 128];
        var geometry = new THREE.Geometry();
        var face_vertex_index = new Int32Array(12);    // Keeps track of which FACE vertex we are on
        /* Loop over field vertex indices, at each index, create the 8 vertices
           corresponding to the current cube, pull the field values at those
           vertices, compare them to the isovalue, and generate the corresponding
           face vertexes where the field value is less than the isovalue. */
        for (let i=0; i<nnx; i++) {
            for (let j=0; j<nny; j++) {
                for (let k=0; k<nnz; k++) {
                    var cube_index = 0;
                    var field_values = new Float32Array(8);
                    var field_xyzs = new Array(8);
                    for (let l=0; l<8; l++) {
                        var offset = cube_vertices[l];
                        var ioff = i + offset[0];
                        var joff = j + offset[1];
                        var koff = k + offset[2]
                        //var field_index = (nz * ioff + joff) * ny + koff
                        var field_index = ioff * ny * nz + joff * nz + koff;
                        field_values[l] = field.values[field_index];
                        field_xyzs[l] = new THREE.Vector3(field.x[ioff], field.y[joff], field.z[koff]);
                        if (field_values[l] > isovalue) {
                            cube_index |= bits[l];
                        };
                    };
                    /* Now that we have the cube_index, we can use the edge_table
                       to lookup the type of face we have to deal with. */
                    var integer = this.edge_table[cube_index];
                    /* If this cube has no intersecting field values, skip
                       adding surface vertices and faces (the continue command
                       means skip the remaining code and go to the next
                       iteration of the loop). */
                    if (integer === 0 || integer === 255) continue;
                    /* If we do have an integer index to use, lets interpolate
                       the face vertices. Along edges of our current field
                       cube where the field values meet the criteria set by the
                       isovalue, we need to linearly interpolate along that
                       edge to find the position of the face's vertex. */
                    var alpha = 0.5;              // linear interpolation parameter
                    for (let m=0; m<12; m++) {    // 12 field cube edges
                        var check = 1 << m;       // 1, 2, 4, 8, ... (bit shift)
                        if (integer & check) {
                            face_vertex_index[m] = geometry.vertices.length;
                            var vertex_pair = cube_edges[m];
                            var a = vertex_pair[0];
                            var b = vertex_pair[1];
                            var xyz_a = field_xyzs[a];
                            var xyz_b = field_xyzs[b];
                            var val_a = field_values[a];
                            var val_b = field_values[b];
                            alpha = (isovalue - val_a) / (val_b - val_a);
                            var vertex = xyz_a.lerp(xyz_b, alpha);
                            geometry.vertices.push(vertex);
                        };
                    };
                    var cur_face_verts = this.tri_table[cube_index];
                    var num_face_verts = cur_face_verts.length;
                    for (let m=0; m<num_face_verts; m+=3) {
                        var i0 = face_vertex_index[cur_face_verts[m]];
                        var i1 = face_vertex_index[cur_face_verts[m+1]];
                        var i2 = face_vertex_index[cur_face_verts[m+2]];
                        var face = new THREE.Face3(i0, i1, i2);
                        geometry.faces.push(face);
                    };
                };
            };
        };
        console.log(geometry.vertices.length);
        console.log(geometry.faces.length);
        console.log(geometry.vertices);
        console.log(geometry.faces);
        geometry.computeFaceNormals();
        geometry.computeVertexNormals();
        var material = new THREE.MeshLambertMaterial({
            color: 0x0000ff,
            side: THREE.DoubleSide
        });
        return new THREE.Mesh(geometry, material);
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

    ThreeJSApp.prototype.edge_table = new Uint32Array([
        0x0  , 0x109, 0x203, 0x30a, 0x406, 0x50f, 0x605, 0x70c,
        0x80c, 0x905, 0xa0f, 0xb06, 0xc0a, 0xd03, 0xe09, 0xf00,
        0x190, 0x99 , 0x393, 0x29a, 0x596, 0x49f, 0x795, 0x69c,
        0x99c, 0x895, 0xb9f, 0xa96, 0xd9a, 0xc93, 0xf99, 0xe90,
        0x230, 0x339, 0x33 , 0x13a, 0x636, 0x73f, 0x435, 0x53c,
        0xa3c, 0xb35, 0x83f, 0x936, 0xe3a, 0xf33, 0xc39, 0xd30,
        0x3a0, 0x2a9, 0x1a3, 0xaa , 0x7a6, 0x6af, 0x5a5, 0x4ac,
        0xbac, 0xaa5, 0x9af, 0x8a6, 0xfaa, 0xea3, 0xda9, 0xca0,
        0x460, 0x569, 0x663, 0x76a, 0x66 , 0x16f, 0x265, 0x36c,
        0xc6c, 0xd65, 0xe6f, 0xf66, 0x86a, 0x963, 0xa69, 0xb60,
        0x5f0, 0x4f9, 0x7f3, 0x6fa, 0x1f6, 0xff , 0x3f5, 0x2fc,
        0xdfc, 0xcf5, 0xfff, 0xef6, 0x9fa, 0x8f3, 0xbf9, 0xaf0,
        0x650, 0x759, 0x453, 0x55a, 0x256, 0x35f, 0x55 , 0x15c,
        0xe5c, 0xf55, 0xc5f, 0xd56, 0xa5a, 0xb53, 0x859, 0x950,
        0x7c0, 0x6c9, 0x5c3, 0x4ca, 0x3c6, 0x2cf, 0x1c5, 0xcc ,
        0xfcc, 0xec5, 0xdcf, 0xcc6, 0xbca, 0xac3, 0x9c9, 0x8c0,
        0x8c0, 0x9c9, 0xac3, 0xbca, 0xcc6, 0xdcf, 0xec5, 0xfcc,
        0xcc , 0x1c5, 0x2cf, 0x3c6, 0x4ca, 0x5c3, 0x6c9, 0x7c0,
        0x950, 0x859, 0xb53, 0xa5a, 0xd56, 0xc5f, 0xf55, 0xe5c,
        0x15c, 0x55 , 0x35f, 0x256, 0x55a, 0x453, 0x759, 0x650,
        0xaf0, 0xbf9, 0x8f3, 0x9fa, 0xef6, 0xfff, 0xcf5, 0xdfc,
        0x2fc, 0x3f5, 0xff , 0x1f6, 0x6fa, 0x7f3, 0x4f9, 0x5f0,
        0xb60, 0xa69, 0x963, 0x86a, 0xf66, 0xe6f, 0xd65, 0xc6c,
        0x36c, 0x265, 0x16f, 0x66 , 0x76a, 0x663, 0x569, 0x460,
        0xca0, 0xda9, 0xea3, 0xfaa, 0x8a6, 0x9af, 0xaa5, 0xbac,
        0x4ac, 0x5a5, 0x6af, 0x7a6, 0xaa , 0x1a3, 0x2a9, 0x3a0,
        0xd30, 0xc39, 0xf33, 0xe3a, 0x936, 0x83f, 0xb35, 0xa3c,
        0x53c, 0x435, 0x73f, 0x636, 0x13a, 0x33 , 0x339, 0x230,
        0xe90, 0xf99, 0xc93, 0xd9a, 0xa96, 0xb9f, 0x895, 0x99c,
        0x69c, 0x795, 0x49f, 0x596, 0x29a, 0x393, 0x99 , 0x190,
        0xf00, 0xe09, 0xd03, 0xc0a, 0xb06, 0xa0f, 0x905, 0x80c,
        0x70c, 0x605, 0x50f, 0x406, 0x30a, 0x203, 0x109, 0x0
    ]);

    ThreeJSApp.prototype.tri_table = [
        [],
        [0, 8, 3],
        [0, 1, 9],
        [1, 8, 3, 9, 8, 1],
        [1, 2, 10],
        [0, 8, 3, 1, 2, 10],
        [9, 2, 10, 0, 2, 9],
        [2, 8, 3, 2, 10, 8, 10, 9, 8],
        [3, 11, 2],
        [0, 11, 2, 8, 11, 0],
        [1, 9, 0, 2, 3, 11],
        [1, 11, 2, 1, 9, 11, 9, 8, 11],
        [3, 10, 1, 11, 10, 3],
        [0, 10, 1, 0, 8, 10, 8, 11, 10],
        [3, 9, 0, 3, 11, 9, 11, 10, 9],
        [9, 8, 10, 10, 8, 11],
        [4, 7, 8],
        [4, 3, 0, 7, 3, 4],
        [0, 1, 9, 8, 4, 7],
        [4, 1, 9, 4, 7, 1, 7, 3, 1],
        [1, 2, 10, 8, 4, 7],
        [3, 4, 7, 3, 0, 4, 1, 2, 10],
        [9, 2, 10, 9, 0, 2, 8, 4, 7],
        [2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4],
        [8, 4, 7, 3, 11, 2],
        [11, 4, 7, 11, 2, 4, 2, 0, 4],
        [9, 0, 1, 8, 4, 7, 2, 3, 11],
        [4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1],
        [3, 10, 1, 3, 11, 10, 7, 8, 4],
        [1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4],
        [4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3],
        [4, 7, 11, 4, 11, 9, 9, 11, 10],
        [9, 5, 4],
        [9, 5, 4, 0, 8, 3],
        [0, 5, 4, 1, 5, 0],
        [8, 5, 4, 8, 3, 5, 3, 1, 5],
        [1, 2, 10, 9, 5, 4],
        [3, 0, 8, 1, 2, 10, 4, 9, 5],
        [5, 2, 10, 5, 4, 2, 4, 0, 2],
        [2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8],
        [9, 5, 4, 2, 3, 11],
        [0, 11, 2, 0, 8, 11, 4, 9, 5],
        [0, 5, 4, 0, 1, 5, 2, 3, 11],
        [2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5],
        [10, 3, 11, 10, 1, 3, 9, 5, 4],
        [4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10],
        [5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3],
        [5, 4, 8, 5, 8, 10, 10, 8, 11],
        [9, 7, 8, 5, 7, 9],
        [9, 3, 0, 9, 5, 3, 5, 7, 3],
        [0, 7, 8, 0, 1, 7, 1, 5, 7],
        [1, 5, 3, 3, 5, 7],
        [9, 7, 8, 9, 5, 7, 10, 1, 2],
        [10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3],
        [8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2],
        [2, 10, 5, 2, 5, 3, 3, 5, 7],
        [7, 9, 5, 7, 8, 9, 3, 11, 2],
        [9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11],
        [2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7],
        [11, 2, 1, 11, 1, 7, 7, 1, 5],
        [9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11],
        [5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0],
        [11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0],
        [11, 10, 5, 7, 11, 5],
        [10, 6, 5],
        [0, 8, 3, 5, 10, 6],
        [9, 0, 1, 5, 10, 6],
        [1, 8, 3, 1, 9, 8, 5, 10, 6],
        [1, 6, 5, 2, 6, 1],
        [1, 6, 5, 1, 2, 6, 3, 0, 8],
        [9, 6, 5, 9, 0, 6, 0, 2, 6],
        [5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8],
        [2, 3, 11, 10, 6, 5],
        [11, 0, 8, 11, 2, 0, 10, 6, 5],
        [0, 1, 9, 2, 3, 11, 5, 10, 6],
        [5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11],
        [6, 3, 11, 6, 5, 3, 5, 1, 3],
        [0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6],
        [3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9],
        [6, 5, 9, 6, 9, 11, 11, 9, 8],
        [5, 10, 6, 4, 7, 8],
        [4, 3, 0, 4, 7, 3, 6, 5, 10],
        [1, 9, 0, 5, 10, 6, 8, 4, 7],
        [10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4],
        [6, 1, 2, 6, 5, 1, 4, 7, 8],
        [1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7],
        [8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6],
        [7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9],
        [3, 11, 2, 7, 8, 4, 10, 6, 5],
        [5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11],
        [0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6],
        [9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6],
        [8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6],
        [5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11],
        [0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7],
        [6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9],
        [10, 4, 9, 6, 4, 10],
        [4, 10, 6, 4, 9, 10, 0, 8, 3],
        [10, 0, 1, 10, 6, 0, 6, 4, 0],
        [8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10],
        [1, 4, 9, 1, 2, 4, 2, 6, 4],
        [3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4],
        [0, 2, 4, 4, 2, 6],
        [8, 3, 2, 8, 2, 4, 4, 2, 6],
        [10, 4, 9, 10, 6, 4, 11, 2, 3],
        [0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6],
        [3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10],
        [6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1],
        [9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3],
        [8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1],
        [3, 11, 6, 3, 6, 0, 0, 6, 4],
        [6, 4, 8, 11, 6, 8],
        [7, 10, 6, 7, 8, 10, 8, 9, 10],
        [0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10],
        [10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0],
        [10, 6, 7, 10, 7, 1, 1, 7, 3],
        [1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7],
        [2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9],
        [7, 8, 0, 7, 0, 6, 6, 0, 2],
        [7, 3, 2, 6, 7, 2],
        [2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7],
        [2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7],
        [1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11],
        [11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1],
        [8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6],
        [0, 9, 1, 11, 6, 7],
        [7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0],
        [7, 11, 6],
        [7, 6, 11],
        [3, 0, 8, 11, 7, 6],
        [0, 1, 9, 11, 7, 6],
        [8, 1, 9, 8, 3, 1, 11, 7, 6],
        [10, 1, 2, 6, 11, 7],
        [1, 2, 10, 3, 0, 8, 6, 11, 7],
        [2, 9, 0, 2, 10, 9, 6, 11, 7],
        [6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8],
        [7, 2, 3, 6, 2, 7],
        [7, 0, 8, 7, 6, 0, 6, 2, 0],
        [2, 7, 6, 2, 3, 7, 0, 1, 9],
        [1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6],
        [10, 7, 6, 10, 1, 7, 1, 3, 7],
        [10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8],
        [0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7],
        [7, 6, 10, 7, 10, 8, 8, 10, 9],
        [6, 8, 4, 11, 8, 6],
        [3, 6, 11, 3, 0, 6, 0, 4, 6],
        [8, 6, 11, 8, 4, 6, 9, 0, 1],
        [9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6],
        [6, 8, 4, 6, 11, 8, 2, 10, 1],
        [1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6],
        [4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9],
        [10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3],
        [8, 2, 3, 8, 4, 2, 4, 6, 2],
        [0, 4, 2, 4, 6, 2],
        [1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8],
        [1, 9, 4, 1, 4, 2, 2, 4, 6],
        [8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1],
        [10, 1, 0, 10, 0, 6, 6, 0, 4],
        [4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3],
        [10, 9, 4, 6, 10, 4],
        [4, 9, 5, 7, 6, 11],
        [0, 8, 3, 4, 9, 5, 11, 7, 6],
        [5, 0, 1, 5, 4, 0, 7, 6, 11],
        [11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5],
        [9, 5, 4, 10, 1, 2, 7, 6, 11],
        [6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5],
        [7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2],
        [3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6],
        [7, 2, 3, 7, 6, 2, 5, 4, 9],
        [9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7],
        [3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0],
        [6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8],
        [9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7],
        [1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4],
        [4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10],
        [7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10],
        [6, 9, 5, 6, 11, 9, 11, 8, 9],
        [3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5],
        [0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11],
        [6, 11, 3, 6, 3, 5, 5, 3, 1],
        [1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6],
        [0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10],
        [11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5],
        [6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3],
        [5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2],
        [9, 5, 6, 9, 6, 0, 0, 6, 2],
        [1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8],
        [1, 5, 6, 2, 1, 6],
        [1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6],
        [10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0],
        [0, 3, 8, 5, 6, 10],
        [10, 5, 6],
        [11, 5, 10, 7, 5, 11],
        [11, 5, 10, 11, 7, 5, 8, 3, 0],
        [5, 11, 7, 5, 10, 11, 1, 9, 0],
        [10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1],
        [11, 1, 2, 11, 7, 1, 7, 5, 1],
        [0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11],
        [9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7],
        [7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2],
        [2, 5, 10, 2, 3, 5, 3, 7, 5],
        [8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5],
        [9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2],
        [9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2],
        [1, 3, 5, 3, 7, 5],
        [0, 8, 7, 0, 7, 1, 1, 7, 5],
        [9, 0, 3, 9, 3, 5, 5, 3, 7],
        [9, 8, 7, 5, 9, 7],
        [5, 8, 4, 5, 10, 8, 10, 11, 8],
        [5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0],
        [0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5],
        [10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4],
        [2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8],
        [0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11],
        [0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5],
        [9, 4, 5, 2, 11, 3],
        [2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4],
        [5, 10, 2, 5, 2, 4, 4, 2, 0],
        [3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9],
        [5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2],
        [8, 4, 5, 8, 5, 3, 3, 5, 1],
        [0, 4, 5, 1, 0, 5],
        [8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5],
        [9, 4, 5],
        [4, 11, 7, 4, 9, 11, 9, 10, 11],
        [0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11],
        [1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11],
        [3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4],
        [4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2],
        [9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3],
        [11, 7, 4, 11, 4, 2, 2, 4, 0],
        [11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4],
        [2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9],
        [9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7],
        [3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10],
        [1, 10, 2, 8, 7, 4],
        [4, 9, 1, 4, 1, 7, 7, 1, 3],
        [4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1],
        [4, 0, 3, 7, 4, 3],
        [4, 8, 7],
        [9, 10, 8, 10, 11, 8],
        [3, 0, 9, 3, 9, 11, 11, 9, 10],
        [0, 1, 10, 0, 10, 8, 8, 10, 11],
        [3, 1, 10, 11, 3, 10],
        [1, 2, 11, 1, 11, 9, 9, 11, 8],
        [3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9],
        [0, 2, 11, 8, 0, 11],
        [3, 2, 11],
        [2, 3, 8, 2, 8, 10, 10, 8, 9],
        [9, 10, 2, 0, 9, 2],
        [2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8],
        [1, 10, 2],
        [1, 3, 8, 9, 1, 8],
        [0, 9, 1],
        [0, 3, 8],
        []
    ];

    return {'ThreeJSApp': ThreeJSApp};
});
