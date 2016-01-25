'use strict';


require.config({
    shim: {
    },
});


define([
    "widgets/js/widget"
], function(widget){
    var HelloView = widget.DOMWidgetView.extend({
        // Render the view.
        render: function(){
            this.$el.text('Hello World from container!');
        },
    });

    //manager.WidgetManager.register_widget_view('HelloView', HelloView);
    return {'HelloView': HelloView};
});
