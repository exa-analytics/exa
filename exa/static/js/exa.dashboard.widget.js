'use strict';


require.config({
    shim: {
        'nbextensions/exa/exa.dashboard': {
            exports: 'dashboard'
        },
    },
});


define([
    'nbextensions/widgets/widgets/js/widget',
    'nbextensions/widgets/widgets/js/manager',
    'nbextensions/exa/exa.dashboard',
    'jquery'
], function(
    widget,
    manager,
    dashboard,
    $
) {
    var DashboardView = widget.DOMWidgetView.extend(dashboard);


    manager.WidgetManager.register_widget_view('DashboardView', DashboardView);
    return {'DashboardView': DashboardView}
});
