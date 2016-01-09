'use strict';

class Dashboard {
    constructor() {};

    render() {
        var self = this;
        console.log('Hello World');
        console.log(self);
    };
};


var dashboard = new Dashboard();


$(document).ready(function(){
    $("#b_click").click(function() {
        dashboard.render();
    });
});
