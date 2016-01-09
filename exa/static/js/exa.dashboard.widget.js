'use strict';


require.config({
    shim: {
        'nbextensions/exa/exa.workspace': {
            exports: 'workspace'
        },
    },
});


define([
    'nbextensions/widgets/widgets/js/widget',
    'nbextensions/widgets/widgets/js/manager',
    'nbextensions/exa/exa.workspace',
    'jquery'
], function(
    widget,
    manager,
    workspace,
    $
) {
    var WorkspaceView = widget.DOMWidgetView.extend(workspace);

    return {'WorkspaceView': WorkspaceView}
});
