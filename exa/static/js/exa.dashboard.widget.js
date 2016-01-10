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
    },
});


define([
    'nbextensions/widgets/widgets/js/widget',
    'nbextensions/widgets/widgets/js/manager',
    'nbextensions/exa/static/js/exa.dashboard'
], function(
    widget,
    manager,
    dashboard
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
        },
    });

    return {'DashboardView': DashboardView}
});
