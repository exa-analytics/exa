'use strict';

var dashboard = {
    constructor: function() {
        console.log('in constructor');
    },

    initialize: function() {
        console.log('in init');
    },

    render: function() {
        console.log('in render');
    },

    containers: function() {
        console.log('how to get containers?');
    },
}


console.log(dashboard);


$(document).ready(function(){
    $("#click_init").click(function() {
        dashboard.initialize();
    });
    $("#click_render").click(function() {
        dashboard.render();
    });
    $("#click_container").click(function() {
        dashboard.containers();
    });
});
