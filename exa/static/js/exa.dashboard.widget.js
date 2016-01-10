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
        }
    },
});


define([
    'nbextensions/widgets/widgets/js/widget',
    'nbextensions/widgets/widgets/js/manager',
    'nbextensions/exa/static/js/exa.dashboard',
    'nbextensions/exa/static/js/exa.dashboard.sidebar.widget'
], function(
    widget,
    manager,
    dashboard,
    sidebar
) {
    var DashboardView = widget.DOMWidgetView.extend({
        /*"""
        Dashboard Widget Application (BackboneJS)
        ```````````````````````````````````````````
        The following code relies on the backbone.js web framework.
        */
        initialize: function() {
            _.bindAll(this, 'render');    // Fixes loss of context for 'this' within methods
            this.render();
        },

        render: function() {
            var self = this;
            console.log(this);
            console.log(this.model);
            console.log(document.getElementsByTagName('*'));
            var obj = $(document.getElementById('header-container'));
            this.width = obj.width();
            this.height = 500;
            this.container = dashboard.create_workspace(this.width, this.height);
            this.sidebar = new sidebar();
            this.container.append(this.sidebar.gui.domElement);
            this.container.append(this.sidebar.gui_style_element);
            console.log(this.sidebar);
            this.setElement(this.container);
        },
    });

    return {'DashboardView': DashboardView}
});
