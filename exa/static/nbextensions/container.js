'use strict';


define(['widgets/js/widget'], function(widget){
    var ContainerView = widget.DOMWidgetView.extend({
        render: function(){
            this.$el.text('Hello World!');
        },
    });

    return {'ContainerView': ContainerView};
});
