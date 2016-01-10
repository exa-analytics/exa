/*"""
Dashboard Application
`````````````````````````````````
This is module provide functionality for both the BackboneJS based
Dashboard application as well as the PolymerJS/AngularJS based Dashboard
application.
*/
'use strict';

var dashboard = {
    create_workspace: function() {
        var container = $('<div/>').width(800).height(600);
        container.css('border', '1px solid black');
        container.css('resize', 'both');
        return container;
    }
};
