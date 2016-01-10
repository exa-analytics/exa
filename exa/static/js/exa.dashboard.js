/*"""
Dashboard Application
`````````````````````````````````
This is module provide functionality for both the BackboneJS based
Dashboard application as well as the PolymerJS/AngularJS based Dashboard
application.
*/
'use strict';

var dashboard = {
    create_workspace: function(width, height) {
        var container = $('<div/>').width(width).height(height).resizable();
        container.css('border', '1px solid black');
        container.css('resize', 'both');
        container.css('width', '100%');
        return container;
    }
};
