'use strict';

class Workspace {
    constructor() {};

    render() {
        var self = this;
        console.log('Hello World');
        console.log(self);
    };
};


var workspace = new Workspace();


$(document).ready(function(){
    $("#b_click").click(function() {
        workspace.render();
    });
});
