/*"""
Dashboard Application (Widget)
``````````````````````````````

*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/static/js/exa.dashboard': {
            exports: 'dashboard'
        },

        'nbextensions/exa/static/js/exa.dashboard.sidebar.widget': {
            exports: 'sidebar'
        },

        'nbextensions/exa/static/js/exa.three': {
            exports: 'threejs'
        }
    },
});


define([
    'nbextensions/widgets/widgets/js/widget',
    'nbextensions/widgets/widgets/js/manager',
    'nbextensions/exa/static/js/exa.dashboard',
    'nbextensions/exa/static/js/exa.dashboard.sidebar.widget',
    'nbextensions/exa/static/js/exa.three'
], function(
    widget,
    manager,
    dashboard,
    sidebar,
    threejs
) {
    var DashboardView = widget.DOMWidgetView.extend({
        /*"""
        Dashboard Widget Application (BackboneJS)
        ```````````````````````````````````````````
        The following code relies on the backbone.js web framework.
        */
        initialize: function() {
            _.bindAll(this, 'render');    // Fixes loss of context for 'this' within methods
            //this.render();
        },

        render: function() {
            var self = this;
            //console.log(document.getElementsByTagName('*'));
            var obj = $(document.getElementById('header-container'));
            this.width = obj.width();
            this.height = 500;
            this.sidebarwidth = 200;
            this.container = dashboard.create_workspace(this.width, this.height);
            this.canvas = dashboard.gen_canvas(this.width, this.height, this.sidebarwidth);
            console.log(this.canvas.width());
            console.log(this.canvas.height());
            this.threejs = new threejs(this.width, this.height, this.canvas);
            //console.log(this.threejs);
            //console.log(this.threejs.scene);
            //console.log(this.threejs);
            this.sidebar = new sidebar(this.sidebarwidth);
            this.container.append(this.sidebar.gui.domElement);
            this.container.append(this.sidebar.gui_style_element);
            this.container.append(this.canvas);
            //this.threejs.render();
            //console.log(this.canvas);
            //console.log(this.sidebar);
            this.setElement(this.container);
            //this.threejs.render();
            this.on('displayed', function () {
                this.canvas.resize();
            //    this.threejs.animate();
            //    this.threejs.controls.handleResize();
            });
        },
    });

    return {'DashboardView': DashboardView}
});
