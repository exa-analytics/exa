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
        'nbextensions/exa/apps/app3d': {
            exports: 'App3D'
        },
    },
});


define([
    'nbextensions/exa/apps/app3d'
], function(App3D) {
    class TestContainer {
        /*"""
        TestContainer
        ==============
        A test application for the container
        */
        constructor(view) {
            this.view = view;
            this.view.create_canvas();
            this.app3d = new App3D(this.view.canvas);
            this.app3d.test_mesh();
            this.app3d.render();
            this.view.container.append(this.view.canvas);
            var view_self = this.view;
            this.view.on('displayed', function() {
                view_self.app.app3d.animate();
                view_self.app.app3d.controls.handleResize();
            });
        };

        resize() {
            this.app3d.resize();
        };
    };

    return TestContainer;
});
