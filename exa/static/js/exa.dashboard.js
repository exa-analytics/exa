/*"""
Dashboard Application
`````````````````````````````````
This is module provide functionality for both the BackboneJS based
Dashboard application as well as the PolymerJS/AngularJS based Dashboard
application.
*/
'use strict';

var dashboard = ({
    create_workspace: function(width, height) {
        var container = $('<div/>').width(width).height(height).resizable({
            aspectRatio: false,
            resize: function(event, ui) {
                self.width = ui.size.width;
                self.height = ui.size.height;
                // self.model.set('width', self.width);
                // self.model.set('height', self.height);
                // self.app.resize(self.width, self.height);
            }
        });
        container.css('border', '1px solid black');
        container.css('background', '#dcdcdc');
        container.css('resize', 'both');
        container.css('width', '100%');
        return container;
    },

    //resize_canvas: function(container, canvas) {
    //},

    //gen_canvas: function(container, sidebarwidth) {
    gen_canvas: function(width, height, sidebarwidth) {
        self.nwidth = (width - sidebarwidth) / width * 100;
        self.sidebarwidth = sidebarwidth;
        var canvas = $('<canvas/>').width(width - sidebarwidth).height(height).resizable({
            aspectRatio: false,
            resize: function(event, ui) {
                self.nwidth = (ui.size.width - self.sidebarwidth) / ui.size.width * 100;
                self.width = ui.size.width * self.nwidth;
                self.height = ui.size.height;
            }
        });
        canvas.css('resize', 'both');
        canvas.css('top', 0);
        canvas.css('left', sidebarwidth);
        canvas.css('width', String(self.nwidth) + '%');
        canvas.css('background', '#999999');
        canvas.css('position', 'absolute');
        canvas.css('height', '100%');
        return canvas;
    }

});
