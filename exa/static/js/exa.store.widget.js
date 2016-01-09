'use strict';


require.config({
    shim: {
        'nbextensions/exa/exa.store': {
            exports: 'store'
        },
    },
});


define([
    'nbextensions/widgets/widgets/js/widget',
    'nbextensions/widgets/widgets/js/manager',
    'nbextensions/exa/exa.store',
    'jquery'
], function(
    widget,
    manager,
    store,
    $
) {
    var StoreView = widget.DOMWidgetView.extend(store);

    return {'StoreView': StoreView}
});
