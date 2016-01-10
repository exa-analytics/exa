/*"""
BackboneJS Based Dashboard
````````````````````````````

*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/static/js/exa.dashboard': {
            exports: 'dashboard'
        },

        'nbextensions/exa/static/js/libs/dat.gui.min': {
            exports: 'dat'
        }
    },
});


define([
    'nbextensions/widgets/widgets/js/widget',
    'nbextensions/widgets/widgets/js/manager',
    'nbextensions/exa/static/js/exa.dashboard',
    'nbextensions/exa/static/js/libs/dat.gui.min'
], function(
    widget,
    manager,
    dashboard,
    dat
) {
    var DashboardView = widget.DOMWidgetView.extend({
        /*"""
        Dashboard Application (BackboneJS)
        `````````````````````````````````
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
            this.container = dashboard.create_workspace();
            this.gui = new dat.GUI({autoPlace: false, width: 300});
            $(this.gui.domElement).css('position', 'absolute');
            $(this.gui.domElement).css('top', 0);
            $(this.gui.domElement).css('right', 0);
            console.log(this.gui);
            this.container.append(this.gui);
            this.setElement(this.container);
        },
    });

    return {'DashboardView': DashboardView}
});
